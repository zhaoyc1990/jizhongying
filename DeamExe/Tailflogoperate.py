# coding:utf-8
import socket

import paramiko
import select
import sys
import os, cStringIO, StringIO
from Execcmd import Cmdpool
from server.models import Server
from host.models import hostinfo
from LogSplit.models import servicename
from django.forms.models import model_to_dict
class Tailflogoperate():
    def __init__(self,serverid):
        self.serverid = serverid

    def execcmd(self, md5, log=None):  #如果想查看容器其它文件可以在此指定log,否则此log为默认
        #先把要执行的文件传到远程主机。为了，能得到运行的PID的所以执行脚本来获得PID更安全
        server_for_log = model_to_dict(servicename.objects.get(id=self.serverid))
        if server_for_log['server'] != None:    #如果有关联的服务，先把关联的服务所需要的条件查出来
            server = model_to_dict(Server.objects.get(id=server_for_log['server']))
            hostinff = model_to_dict(hostinfo.objects.get(id=server['server_host']))     #查找关联服务的所在主机
            if server['container_id'] == True:            #判断是否有容器ID来断定是否在容器里
                if hostinff['forward_host'] != None: # 不等于空，则需要跳板机
                    hostinf = model_to_dict(hostinfo.objects.get(id=hostinff['forward_host']))
                    #组装要执行的bash脚本
                    bashfile = Cmdpool(md5).forward_docker_tailf_log(server['container_id'], server_for_log['log_path'],
                                                                     hostinff['ip'], hostinff['sshport'], hostinff['rootuser'], hostinff['rootpassword'])
                else:  #如在容器里，但不需要跳板
                    bashfile = Cmdpool(md5).docker_tailf_log(server['container_id'], server_for_log['log_path'])
            elif hostinff['forward_host'] != None:   #如果不在容器里，但需要跳板机
                hostinf = model_to_dict(hostinfo.objects.get(id=hostinff['forward_host']))
                bashfile = Cmdpool(md5).forward_tailf_log(server_for_log['log_path'],
                                                          hostinff['ip'], hostinff['sshport'], hostinff['rootuser'],
                                                          hostinff['rootpassword'])
            else:
                hostinf = hostinff
                bashfile = Cmdpool(md5).tailf_log(server_for_log['log_path'])
        else:
            hostinff = model_to_dict(hostinfo.objects.get(id=server_for_log['host']))
            if hostinff['forward_host'] != None:
                hostinf = model_to_dict(hostinfo.objects.get(id=hostinff['forward_host']))  #数据库查询跳板机信息
                if server_for_log['is_container'] == True:  #需要跳板机，并在容器里
                    bashfile = Cmdpool(md5).noserver_forward_docker_tailf_log(server_for_log['log_path'], server_for_log['port'], hostinff['ip'],
                                                                              hostinff['sshport'], hostinff['rootname'], hostinff['rootpassword'])
                else:
                    bashfile = Cmdpool(md5).noserver_forward_tailf_log(server_for_log['log_path'], hostinff['ip'],
                                                                              hostinff['sshport'], hostinff['rootname'], hostinff['rootpassword'])
            else: #不需要跳板机
                hostinf = hostinff
                if server_for_log['is_container'] == True:  #服务在容器里
                    bashfile = Cmdpool(md5).noserver_docker_tailf_log(server_for_log['log_path'], server_for_log['port'])
                else:
                    bashfile = Cmdpool(md5).tailf_log(server_for_log['log_path'])

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            print u"连接主机:" , hostinf['ip']
            ssh.connect(hostinf['ip'], int(hostinf['sshport']), hostinf['rootname'], hostinf['rootpassword'], timeout=5)
        except socket.timeout: # 如果 主机连接 不上就返回None
            return None
        f = cStringIO.StringIO()
        f.write(bashfile)
        f.seek(0)  #因为文件写入字符串后，文件指针在最后面了， 所以需要seek 0 把指针放在文件第一个字符前
        t = paramiko.Transport((hostinf['ip'],hostinf['sshport']))
        t.connect(username=hostinf['rootname'], password=hostinf['rootpassword'])
        sftp = paramiko.SFTPClient.from_transport(t)
        try:
            sftp.putfo(f, os.path.join('/tmp/', md5 + '.sh'))
        except IOError, e:
            sftp.putfo(f, os.path.join('/tmp/', md5 + '.sh'))
            raise IOError(e)
        finally:
            t.close()
        #开启session传输接口
        return ssh
        transport = ssh.get_transport()
        channel = transport.open_session()
        channel.exec_command('bash /tmp/' + md5 + '.sh')
        print u"准备return"
        while 1:
            if channel.exit_status_ready():
                break
            try:
                rl, _, _ = select.select([channel], [], [], 1)
                if len(rl) > 0:
                    recv = channel.recv(65536)
                    print recv,

            finally:  # KeyboardInterrupt
                print 'got ctrl+c'
                channel.send("\x03")  # 发送 ctrl+c
                channel.close()
                ssh.close()
                exit(0)
                break
    def killcmd(self, md5):
        server_for_log = model_to_dict(servicename.objects.get(id=self.serverid))
        hostinf = model_to_dict(hostinfo.objects.get(id=server_for_log['host']))
        if hostinf['forward_host'] != None:
            hostinf = model_to_dict(hostinfo.objects.get(id=hostinf['forward_host']))
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostinf['ip'], int(hostinf['sshport']), hostinf['rootname'], hostinf['rootpassword'], timeout=5)
        cmd = 'ls -l /tmp/' + md5 + '.pid'
        stdin, stdout, stderr = ssh.exec_command(cmd)   #首先查看是否有这个临时文件
        print u"查看临时文件:", cmd
        out = stdout.readlines()
        if out == []:
            print u"没有找到运行时的PID文件，可能并没有运行tial log.log，或者被删除"
            return 1
        else:
            print out
        cmd = 'kill $(ps -ef | grep `cat /tmp/' + md5 + '.pid` | grep -v grep | awk \'{print $2}\')'
        stdin, stdout, stderr = ssh.exec_command(cmd)
        print u"执行指令：", cmd
        print u"标准出错信息:", stderr.readlines()
        channel = stdout.channel
        cmd = 'rm -rf /tmp/' + md5 + ".pid"
        ssh.exec_command(cmd)
        cmd = 'rm -rf /tmp/' + md5 + ".sh"
        ssh.exec_command(cmd)
        status = channel.recv_exit_status()
        ssh.close()
        return status
    def close(self):
        try:
            self.ssh.close()
        except Exception:
            pass

if __name__ == '__main__':
    tailf = Tailflogoperate(sys.argv[1])
    try:
        log = sys.argv[3]
    except IndexError:
        tailf.execcmd(sys.argv[2])
    else:
        tailf.execmd(sys.argv[2],sys.argv[3])