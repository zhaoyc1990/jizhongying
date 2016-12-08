# coding:utf-8
import os, json
import random
import time
from io import BytesIO

from django.db import OperationalError
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.datastructures import MultiValueDictKeyError
from django.views.decorators.csrf import csrf_exempt
from docker import Client
from docker.errors import APIError
from DeamExe.Dockeroperate import Dockeroperate
from DeamExe.Gitopera import Gitopera
from host.models import Group, hostinfo
from server.models import Environment, HttpChannel, Server

LogFile = os.path.normpath(os.getcwd() + '/logs/consloe.log')
#待定闺中
def server(request):

    return render(request, 'server.html', )

def addserver(request):

    # 先定义一个字典包含上级页面所有name,以便遍历使用
    html_name = {
        'name_Zh': '',  # 服务中文名
        'name_En': '',  # 服务英文名
        'group':'',		#运行服务宿主主机所在组
        'host': '',  # 运行服务宿主主机名
        'environment': '',  # 运行环境选择
        'container': '',  # 是否需要容器化
        'tag': '',  # 环境版本如.java1.6/1.7/1.8
        'port': '',  # 如需要需要容器，则开放端口号,list
        'gitsite': '',  # GIT版本控制地址
        'symbol': '',  # key与value 的赋值符号 :/=
        'filetype': '',  # 配置文件类型(不代表文件后缀)	json/txt
        # 'configure_key':[],	#配置文件 key
        # 'configure_value':[],#配置文件 value
    }
    message = ''
    group_dict = {}
    # 从数据库查寻组名和ID
    for g in Group.objects.all():
        group_dict.update(g.getall())

    env_tuple = ()
    for env in  Environment.objects.values_list('id','env_name'):
        env_tuple = env_tuple + env
    # 从数据库取出环境名，不带tag
    environment = tupletodict(env_tuple)
    if request.method == 'POST':
        try: #如果没选中容器化就没必要去port端口做任何事情
            if request.POST.get('container','') == u'False':
                del html_name['port']
        except:
            pass
        #遍历html_name 给addserver_from赋值
        for key in html_name:
            html_name[key] = request.POST.get(key,'')
            # print(type(html_name[key]))
            # print(key + ":" + html_name[key])

        #存放POST过来的被选中的主机
        host_checked = {}
        #存放post过来的被选中的组名
        group_checked = {}
        environment_checked = {}
        tag_checked = {}
        nothing = ''


        if html_name['environment'] != u'None' and html_name['group'] != u'':
            for envv in Environment.objects.filter(id=int(html_name['environment'])):
                environment_checked = envv.getIdAndName()
                if html_name['tag'] != u'':
                    tag_checked = {html_name['tag']:html_name['tag']}
                #有一个小BUG ，POST过后，只显示POST传过来的版本号，后期加上
        else:
            nothing = '---------'

        for k ,v in html_name.items():
            if v == '' or v == u'' or v == u'None':
                #有空的就返回，重新填写
                message = '除了配置文件，其它项，为必填项'
                if html_name['group'] != u'None' and html_name['group'] != u'':
                    group_checked = getmechecked(group_dict, html_name['group'])
                    if html_name['host'] != u'':
                        # 返回选中的组下面的主机字典
                        hosts = getMeGroupUser(int(html_name['group']))
                        # 把选中的主机挑出来
                        host_checked = getmechecked(hosts, html_name['host'])
                        html_name['host'] = hosts

                else:
                    nothing = '---------'
                html_name['group'] = group_dict
                html_name['environment'] = environment
                return render(request, 'addserver.html', {'html_name': html_name, 'group_checked': group_checked,
                                                          'host_checked': host_checked, 'environment_checked':environment_checked,
                                                          'tag_checked':tag_checked, 'nothing':nothing, 'message':message})
        # 因为configure_key 和value 是配对的list 所以它俩单独遍历
        #添加服务页面并不对配置参数做任何验证
        #######----------开始操作配置文件----------------------------------#
        i = 0
        configure_str = ''
        newline = request.POST.get('symbol','')
        if newline == u'True':
            newline = '\n'
        elif newline == u'False':
            newline = '\r\n'
        else:
            newline = '\r\n'
        while True:
            i = i + 1
            try:
                if request.POST['configure_key' + str(i)] == u'':
                    break
                configure_str=request.POST['configure_key' + str(i)] + '=' + request.POST['configure_value' + str(i)] + request.POST.get('symbol','') + newline
            except MultiValueDictKeyError:
                break
        print "configure_str:", configure_str

        try:
            serverid = Server.objects.create(name_Zh=html_name['name_Zh'], name_En=html_name['name_En'], server_host_id=html_name['host'],
                              is_container=html_name['container'], server_environment_id=html_name['environment'],
                              port=html_name['port'], gitsite=str(html_name['gitsite']),curr_env_tag=html_name['tag'])
        except KeyError:
            serverid = Server.objects.create(name_Zh=html_name['name_Zh'], name_En=html_name['name_En'],
                                             server_host_id=html_name['host'],
                                             is_container=html_name['container'],
                                             server_environment_id=html_name['environment'], gitsite=str(html_name['gitsite']),
                                             curr_env_tag=html_name['tag'])
        serverid = serverid.id
        message = 'success'
        print message
        randomm =  random.randint(1, 10000)
        return render(request, 'addserver.html', {'html_name': html_name, 'message':message,'serverid':serverid, 'random':randomm})
    else:
        html_name['group'] = group_dict
        html_name['environment'] = environment
        return render(request, 'addserver.html', {'html_name': html_name, 'nothing':'---------'})

import subprocess
#服务添加	tchcode.
def gitclone(randomm, gitsite):
    HttpChannelmessage(randomm, 'Begining git download...')
    try:
        git_cmd = ['python DeamExe/Gitopera.py clone ' + gitsite]
        for cmd in git_cmd:
            # 返回标准输出信息
            returnCode = subprocess.check_output(cmd, shell=True)
    except subprocess.CalledProcessError, e:
        HttpChannelmessage(randomm, '执行 git clone 出错')
        HttpChannelmessage(randomm, 'Error')
        print e
        return
    HttpChannelmessage(randomm, returnCode)
    print u'已完成'

def HttpChannelmessage(randomm, message):
    HttpChannel.objects.create(message=message, random=randomm)
from requests.exceptions import ConnectionError


#服务添加	two.
#host 宿主机id			is_container  boolean 是否容器化
#environment			镜像地址比如 192.168.2.246:5000/busybox
#env_tag				镜像表签 latest	1.0
def dockerinit(randomm, host, is_container, environment, env_tag):
    HttpChannelmessage(randomm, '连接主机>>>')
    hostt = hostinfo.objects.values('ip','docker_remote_api_port').filter(id=host)
    env_image = Environment.objects.values('image').filter(id=environment)
    #取出是对象,必须遍历才能得到dict
    for host in hostt:
        pass
    for image in env_image:
        pass

    print 'docker_remote_api_port:' , str(host['docker_remote_api_port'])
    if is_container == 'True':
        cli = Client(base_url='tcp://' + host['ip'] + ":" + str(host['docker_remote_api_port']).strip(),timeout=2)
        i = 0
        returnCode = cli.pull(image['image'],tag=env_tag)#
        try:

            if 'Error' in str(returnCode):
                HttpChannel.objects.create(random=randomm,message=returnCode)
            else:
                HttpChannelmessage(randomm, '推送镜像已完成')
        except OperationalError:
            HttpChannelmessage(randomm, '数据库错误005')
            HttpChannelmessage(randomm, 'Error')
            # HttpChannel.objects.create(message=json.dumps(json.loads(line), indent=4))
    # HttpChannel.objects.create(message=str({'message': 'success'}))

#服务添加  one.
@csrf_exempt
def startinit(request):
    message = {'message':''}
    html_name = {
        'id':'',
        'host':'',
        'container':'',
        'environment':'',
        'tag':'',
        'gitsite':'',
        'random':''
    }
    for key in html_name:
        html_name[key] = request.GET.get(key, '')
        print key + ":get:" + html_name[key]
        if html_name[key] == '':
            return JsonResponse({'message':'Error:'+ key + ' not Null'})

    print u"开始初始化"

    print "Start...."
    try:
        dockerinit(html_name['random'], html_name['host'], html_name['container'], html_name['environment'], html_name['tag'])
        gitclone(html_name['random'], html_name['gitsite'])
        message['message'] = 'success'
        HttpChannelmessage(html_name['random'], 'success')
    except ConnectionError ,ee:
        print u"连接宿主机超时"
        HttpChannelmessage(html_name['random'], '连接宿主机错误003')
        print ee
        print html_name['id']
        print type(html_name['id'])
        bab_server = Server.objects.filter(id=int(html_name['id']))
        bab_server.delete()
        HttpChannelmessage(html_name['random'], 'Error')
        message['Error'] = 'Error'
    return JsonResponse(message)

# http jquery 过来调用的函数 每3秒执行一次 返回数据库未读的消息
@csrf_exempt
def Jquery_get_message(request, randomm):
    message = HttpChannel.objects.filter(take_out=False,random=randomm).order_by('id')
    p = {}; i = 0;
    if message.exists():
        for mess in message:
            p[i] = (mess.getmessage())
            mess.take_out = True
            mess.save()
            i = i+1
    else:
        print u"初始化镜像和代码库过程：暂无新消息01"
        return JsonResponse({'message':'>>>'})
    return JsonResponse(p)


# 慢执行
@csrf_exempt
def deploy(request):
    if request.method == 'POST':
        html_name = {
            'server_id':'',
            'tag':'',
            'randomm':''
        }
        for key in html_name:
            html_name[key] = request.POST.get(key,'')
        for key, value in html_name.items():
            print key + ":" + value
            if value == '':
                return JsonResponse({'message':'参数呢？'})
        # 随机数message 表识
        randomm = html_name['randomm']

        #存放容器ID
        contarner_idd = ''
        # 切换代码 tag

        # 压缩代码
        server = Server.objects.filter(id=html_name['server_id'])
        if server.exists():
            p = {}
            for filterr in server.values('name_En','server_host','gitsite','is_container','server_environment','port','curr_env_tag'):
                p.update(filterr)
            h = {}
            for hostt in hostinfo.objects.values('ip','docker_remote_api_port','host_status').filter(id=int(p['server_host'])):
                h.update(hostt)
            e = {}
            for ee in Environment.objects.values('image').filter(id=p['server_environment']):
                e.update(ee)
            imagesname = '192.168.2.246:5000/' + p['name_En'].lower() + ":" + html_name['tag']
            try:
                cmdd = 'python DeamExe/Compressioncode.py ' + p['gitsite'] + " "+ html_name['tag']
                returnCode = subprocess.check_output(cmdd, shell=True)
                if 'Error' in returnCode:
                    raise Exception
            except subprocess.CalledProcessError, e:
                print e
                print u'Error:执行打包代码错误'
                HttpChannelmessage(randomm,'Error:执行打包代码错误')
                return JsonResponse({'message':'Error'})
            # 下版本将根据项目类型如 比如需要编译。编译后打包格式,构建时是否需要自动解压
            HttpChannelmessage(randomm, 'OK:版本打包完成')
            project_name = Gitopera().getproject(p['gitsite'])
            urll = request.get_raw_uri()
            urlll = request.path
            codefile = urll[:urll.find(urlll)] + "/upload/?filename=" + project_name + '.tar.gz'
            dockerfile = '''
            FROM ''' + e['image'] + ":" + p['curr_env_tag'] + '''
            ADD ''' + codefile + ' /cihi/run/' + project_name + '''.tar.gz
            RUN tar -zxf /cihi/run/''' + project_name + '''.tar.gz -C /cihi/run/
            ENV TZ Asia/Shanghai
            CMD /tmp/start
            '''
            f = BytesIO(dockerfile.encode('utf-8'))
            cli = Client(base_url='tcp://' + h['ip'] + ':' + str(h['docker_remote_api_port']))
            response = [line for line in cli.build(fileobj=f, rm=True, tag=imagesname)]
            if 'Successfully'in response[-1]:
                HttpChannelmessage(randomm,'OK:镜像构建成功')
                # 如最后一个列表包括'Success'字样 ，说明 成功构建,接下来创建容器并启动
                #1.先把API port 内部端口：宿主机端口  所以需要 把p['port']的key 和value 反转一下
                #p['port']反转后结构不变，ports 为容器内部绑定端口

                ofport = evall(p['port'])
                print "port:::::::::" , ofport
                ofport, ports = reverse(ofport)
                print u'反转后::::::::', ofport, ports
                host_conf = cli.create_host_config(restart_policy={'Name':'always'},port_bindings=ofport)
                responsed = cli.create_container(image=imagesname, host_config=host_conf,
                                              environment={"TZ": "Asia/Shanghai"},
                                               ports=ports)
                #2.获取返回信息的ID 启动
                contarner_idd = responsed['Id']
                print '...................', responsed
                # ID存放数据库 当前代码版本号
                print contarner_idd, '................................'
                for serverr in server:
                    serverr.container_id = contarner_idd
                    serverr.curr_tag = html_name['tag']
                serverr.save()
                try:
                    status = cli.start(container=contarner_idd)
                except APIError, e:
                    # 出错后会出现<none>无效镜像和容器，下版本要自动处理
                    HttpChannelmessage(randomm, e.__str__() + '<br>Error::启动错误<br>会出现一些无效镜像，暂时请手动清除')
                    return JsonResponse({'message': 'Error:启动错误'})
                if status == None:
                    print 'contarner_id:', type(contarner_idd[:9])
                    HttpChannelmessage(randomm,'OK:Id:' + str(contarner_idd[:9]) + u'容器启动成功')
                    HttpChannelmessage(randomm,'success')
                    return JsonResponse({'message': 'success'})
                else:
                    HttpChannelmessage(randomm, 'Error::启动错误')
                    return JsonResponse({'message':'Error:启动错误'})
            else:
                HttpChannelmessage(html_name['randomm'],'Error'+ str(response))
                return JsonResponse({'message':'Error' + str(response)})

    else:
        return JsonResponse({'message':' '})

def rst_container(request,action, server_id, randomm):
    # 数据库操作没做
    for container_id in Server.objects.values('container_id').filter(id=server_id):
        pass
    cli = Dockeroperate(server_id,randomm)
    if action == 'restart':
        return_Code = cli.container_restart(container_id['container_id'])
    elif action == 'start':
        return_Code = cli.start_container(container_id['container_id'])
    elif action == 'stop':
        return_Code = cli.container_stop(container_id['container_id'])
    return HttpResponse(
        return_Code['message']
    )


def jsontest(reqest):
    a = 'wocao'
    b = 'hello'
    c = a + '=' + b + '\r\n' + a + '=' + b + '\r\n'
    return HttpResponse(c)
    # return JsonResponse({'message':'success'})


def rm_server(request):
    html_name = {
        'server_id':'',
        'random':''
    }
    for key in html_name:
        html_name[key] = request.GET.get(key,'')
        if html_name[key] == '':
            return JsonResponse({'message':'Error:参数不能为空'})

    dockerr = Dockeroperate(html_name['server_id'],html_name['random'])
    for id in Server.objects.values('container_id').filter(id=html_name['server_id']):
        pass
    if id['container_id'] == '' or id['container_id'] == None:
        Server.objects.get(id=html_name['server_id']).delete()
        HttpChannelmessage(html_name['random'], 'success')
        return JsonResponse({'message': 'success'})
    if dockerr.container_stop(str(id['container_id']))['message'] == 'success':
        if dockerr.container_rm(str(id['container_id']))['message'] == 'success':
            #容器删除后，对数据库操作删除动作
            Server.objects.get(id=html_name['server_id']).delete()
            HttpChannelmessage(html_name['random'], 'success')
            return JsonResponse({'message':'Error:删除成功'})
    else:
        return JsonResponse({'message':'Error:删除失败'})

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
        value[p_list[i]] = p_list[i+1]
        i = i +2
    return value

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
        {},0


def version_switch(request):
    Dockeroperate().test()
    return HttpResponse(
        str(request.get_host() + ":" + request.get_port() + "<br>")
         + str(request.get_raw_uri() + "<br>" + request.get_full_path())

    )



# 取出POST页面选中的select type(dict)
def getmechecked(checked_dict, html_name_key):

    html_name_checked = {}  # 临时存放被选中的组名信息
    group_id = str(html_name_key)
    html_name_checked[group_id] = checked_dict[group_id]
    return html_name_checked



#从数据库取出指定组ID的主机type(json) jquery 专用
@csrf_exempt
def getMeGroupUserJson(request):
    id = request.POST.get('id','')
    if id != '':
        print "id:", id
        p = {}
        print hostinfo.objects.filter(group=id)
        for host in hostinfo.objects.filter(group=id):
            p.update(host.getid())
        return JsonResponse(p)

# 从数据库取出指定组ID的主机type(json) jquery 专用
@csrf_exempt
def getMeEnvTags(request):
    id = request.POST.get('id', '')
    if id != '':
        print "id:", id
        p = {}
        print Environment.objects.filter(id=id)
        for env in Environment.objects.filter(id=id):
            for tag in env.gettags():
                p.update({tag:tag})
    return JsonResponse(p)

# 获取版本号列表
@csrf_exempt
def getservertags(request, server_id):
    if server_id == '':
        return JsonResponse({'message':'参数传递不完整'})
    else:
        p = {}
        for gitsite in Server.objects.values('gitsite').filter(id=server_id):
            p.update(gitsite)
    try:
        git_cmd = 'python DeamExe/Gitopera.py tags ' + p["gitsite"]
            # 返回标准输出信息
        returnCode = subprocess.check_output(git_cmd, shell=True)
    except subprocess.CalledProcessError, e:
        print e
        return JsonResponse({'messgae':'Error'})
    print 'git tags returnCode:', returnCode
    p = {}
    for tag in  returnCode.strip().split("\n"):
        tag = tag.strip()
        p[tag] = tag
    print p
    return JsonResponse(p)
#从数据库取出指定组ID的主机type(dict)
def getMeGroupUser(id):
    pp = {}
    for host in hostinfo.objects.filter(group=id):
        pp.update(host.getid())
    return pp


#把成对的元组，转换成dict
def tupletodict(tup):
    todict = {}
    x = 0
    try:
        for i in range(len(tup)/2):
            todict.update({tup[x]:tup[x+1]})
            x = x+2
    except IndexError:
        print "不是一个成对的tuple"
    return todict