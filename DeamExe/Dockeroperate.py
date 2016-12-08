# coding: utf-8
#!/usr/bin/env python
import subprocess

from docker import Client
from io import BytesIO

from docker.errors import APIError

from DeamExe.Gitopera import Gitopera
from server.models import hostinfo, Server, Environment, HttpChannel


class Dockeroperate:

    def __init__(self,server_id, randomm, tag=None, cli=None):
        self.server_id = server_id
        self.randomm = randomm
        self.tag = tag
        self.cli = cli
        self.port_str = ''
        self.imagename = ''
        self.container = ''

    def build(self, server_id=None, host_id=None):
        if server_id != None:
            self.server_id = server_id
        server = Server.objects.filter(id=self.server_id)
        if server.exists():
            p = {}
            for filterr in server.values('name_En', 'server_host', 'gitsite', 'is_container', 'server_environment',
                                         'port', 'curr_env_tag'):
                p.update(filterr)
            self.port_str = p['port']
            h = {}
            if host_id != None:     #服务迁移时，用于判断
                p['server_host'] = host_id
            for hostt in hostinfo.objects.values('ip', 'docker_remote_api_port', 'host_status').filter(
                    id=int(p['server_host'])):
                h.update(hostt)
            e = {}
            for ee in Environment.objects.values('image').filter(id=p['server_environment']):
                e.update(ee)
            self.imagename = '192.168.2.246:5000/' + p['name_En'].lower() + ":" + self.tag
            try:
                cmdd = 'python DeamExe/Compressioncode.py ' + p['gitsite'] + " " + self.tag
                returnCode = subprocess.check_output(cmdd, shell=True)
                if 'Error' in returnCode:
                    raise Exception(returnCode)
            except subprocess.CalledProcessError, e:
                print e
                print u'Error:执行打包代码错误'
                self.HttpChannelmessage(self.randomm, 'Error:执行打包代码错误')
                return False, {'message': 'Error'}
            # 下版本将根据项目类型如 比如需要编译。编译后打包格式,构建时是否需要自动解压
                self.HttpChannelmessage(self.randomm, 'OK:版本打包完成')
            project_name = Gitopera().getproject(p['gitsite'])
            urll = self.request.get_raw_uri()
            urlll =self.request.path
            codefile = urll[:urll.find(urlll)] + "/upload/?filename=" + project_name + '.tar.gz'
            dockerfile = '''
        			FROM ''' + e['image'] + ":" + p['curr_env_tag'] + '''
        			ADD ''' + codefile + ' /cihi/run/' + project_name + '''.tar.gz
        			RUN tar -zxf /cihi/run/''' + project_name + '''.tar.gz -C /cihi/run/
        			ENV TZ Asia/Shanghai
        			CMD /tmp/start
        			'''
            f = BytesIO(dockerfile.encode('utf-8'))
            self.cli = Client(base_url='tcp://' + h['ip'] + ':' + str(h['docker_remote_api_port']))
            response = [line for line in self.cli.build(fileobj=f, rm=True, tag=self.imagename)]
            # 如最后一个列表包括'Success'字样 ，说明 成功构建,接下来创建容器并启动
            if 'Successfully' in response[-1]:
                self.HttpChannelmessage(self.randomm, str(response[-1]))
                self.HttpChannelmessage(self.randomm, 'OK:镜像构建成功')
                # 构建成功，判断是否有迁移动作
                if host_id != None:
                    for html_name in server: # 配置文件 没有处理
                        Server.objects.create(name_Zh=html_name['name_Zh'], name_En=html_name['name_En'],
                                                         server_host_id=host_id,
                                                         is_container=html_name['container'],
                                                         server_environment_id=html_name['environment'],
                                                         port=html_name['port'], gitsite=str(html_name['gitsite']),
                                                         curr_env_tag=html_name['tag'])

                return True, {'message':str(response[-1])}
            else:
                HttpChannelmessage(html_name['randomm'], 'Error' + str(response))
                return False, {'message':'Error'}



    # config 未来添加功能
    def create_container(self,config=None):
        ofport = self.evall(self.port_str)  #去除空格和制表符。返回dict 类型
        print "port:::::::::", ofport
        # 先把API port 内部端口：宿主机端口  所以需要 把p['port']的key 和value 反转一下,
        # p['port']反转后结构不变，ports 为容器内部绑定端口
        ofport, ports = self.reverse(ofport)
        host_conf = self.cli.create_host_config(restart_policy={'Name': 'always'}, port_bindings=ofport)
        try:
            responsed = self.cli.create_container(image=self.imagename, host_config=host_conf,
                                         environment={"TZ": "Asia/Shanghai"},
                                         ports=ports)
        except APIError, e:
            return False, e.__str__()
        # 2.获取返回信息的ID 启动
        for serverr in Server.objects.filter(id=self.server_id):
            serverr.container_id = str(responsed['Id'])
            serverr.curr_tag = self.tag
            # ID存放数据库 当前代码版本号
        serverr.save()
        return True, str(responsed['Id'])


    def start_container(self, contarner_id, server_idd=None, restart=False, stop=False, rm_con=False, rm_ima=False):
        if self.cli == None and self.server_id != None:
            for host_id in Server.objects.filter(id=self.server_id).values('server_host'):
                host_id = host_id['server_host']
            for host in hostinfo.objects.values('ip','docker_remote_api_port').filter(id=host_id):
                pass
            self.cli = Client(base_url='tcp://' + str(host['ip']) + ':' + str(host['docker_remote_api_port']), timeout=2)
        try:
            if restart:
                sigln = '容器重启'
                status = self.cli.restart(container=contarner_id)
            elif stop:
                sigln = '容器停止'
                status = self.cli.stop(container=contarner_id)
            elif rm_con:
                sigln = '容器删除'
                status = self.cli.remove_container(container=contarner_id)# 不删除 link -v
            elif rm_ima:
                sigln = '镜像删除'
                status = self.cli.remove_image(image=contarner_id)
            else:
                sigln = '容器启动'
                status = self.cli.start(container=contarner_id)
        except APIError, e:
            if 'No such container'in e.__str__():
                self.HttpChannelmessage(self.randomm, 'Waining:\"' + sigln + '\"宿主机没有Id为' + contarner_id[:9] + '的容器')
                return {'message': 'success'}
            # 出错后会出现<none>无效镜像和容器，下版本要自动处理
            else:
                self.HttpChannelmessage(self.randomm, e.__str__() + '<br>Error::'+sigln+'错误<br>会出现一些无效镜像，暂时请手动清除')
            return {'message': 'Error:' + sigln + '错误'}
        if status == None:
            print 'contarner_id:', type(contarner_id[:9])
            self.HttpChannelmessage(self.randomm, 'OK:Id:' + str(contarner_id[:9]) + sigln + '成功')
            return {'message': 'success'}
        else:
            from server.views import HttpChannelmessage
            HttpChannelmessage(self.randomm, 'Error::' + sigln + '错误')
            return {'message': 'Error:' + sigln + '错误'}

    def container_restart(self, contarnet_id, server_idd=None):
        return self.start_container(contarner_id=contarnet_id,server_idd=server_idd, restart=True)

    def container_stop(self, contarnet_id, server_idd=None):
        return self.start_container(contarner_id=contarnet_id,server_idd=server_idd, stop=True)

    def container_rm(self, contarnet_id, server_idd=None):
        return self.start_container(contarner_id=contarnet_id,server_idd=server_idd, rm_con=True)

    def image_rm(self, image_id):
        return self.start_container(contarner_id=image_id, rm_ima=True)
    # 强制部署
    def enforce_deploy(self, contarnet_id, server_idd=None):
        if server_idd != None:
            self.server_id = server_idd
            for host_id in Server.objects.filter(id=server_idd).values('server_host'):
                host_id = host_id['server_host']
            for host in hostinfo.objects.values('ip','docker_remote_api_port').filter(id=host_id):
                pass
            self.cli = Client(base_url='tcp://' + host['ip'] + ':' + host['docker_remote_api_port'], timeout=2)
        status = self.container_stop(contarnet_id=contarnet_id)
        self.HttpChannelmessage(self.randomm, '容器已停止')
        if status['message'] == 'success':
            reqonsed = self.cli.inspect_container(container=contarnet_id)
            reqonsedd = str(reqonsed['Images']).split(':')[1]
            self.container_rm(contarnet_id=contarnet_id)
            self.HttpChannelmessage(self.randomm, '容器已删除')
            self.image_rm(image_id=reqonsedd)
            self.HttpChannelmessage(self.randomm, '镜像已删除')
            # 容器和镜像也删除 开始重建
            ok, info = self.build()
            self.HttpChannelmessage(self.randomm, '重构镜像推送成功')
            if ok:
                # 里面要做数据库查询看有没有额外 配置
                ok, contarnet_id = self.create_container()
                self.HttpChannelmessage(self.randomm, '创建容器已成功')
                if ok:
                    info = self.start_container()
                    self.HttpChannelmessage(self.randomm, '启动容器:' + str(info))
                    return info
                else:
                    self.HttpChannelmessage(self.randomm, 'Error:创建容器出错')
                    return {'message':'Error:创建容器出错'}
            else:
                self.HttpChannelmessage(self.randomm, 'Error:重构镜像失败')
                return info

    # 迁移服务
    # 需要参数host_id 主机id 唯一标识
    def Migrate_container(self,host_id):
        return self.build(host_id=host_id)
        pass







    def HttpChannelmessage(self, randomm, message):
        HttpChannel.objects.create(message=message, random=randomm)
# 把数据库里存放的port 80:90   555:666 转换为dickt {80:90,555:666}
    def evall(ppp):
        p_str = ppp
        p_list = []
        key = 0
        value = {}
        k = 1
        for i in range(len(p_str)):
            try:
                c = int(p_str[i])
                key = key * k + c
                k = 10
            except ValueError:
                if key != 0:
                    p_list.append(key)
                k = 1
                key = 0
        if key != 0:
            p_list.append(key)
        i = 0
        while i < len(p_list):
            value[p_list[i]] = p_list[i + 1]
            i = i + 2
        return value
    # dict key and value 反转
    def reverse(pp):
        if type(pp) is dict:
            if pp != {}:
                cc = {}
                keys = []
                for key, value in pp.items():
                    cc[int(value)] = int(key)
                    keys.append(int(value))
                return cc, keys
        else:
            {}, 0

                    # def test(self):
    #     host = hostinfo.objects.all()
    #     if host.exists():
    #         for hostt in host:
    #             print type(hostt)
    #             print hostt

# if __name__ == '__main__':
#     docker1 = Dockeroperate()
#     docker1.test()