# coding:utf-8
import cgi
import json
import subprocess
import time

import django
from channels import Group
import select
from DeamExe.Tailflogoperate import Tailflogoperate
from channels.auth import channel_session_user_from_http, channel_session_user
from server.models import Channelforlog

# The "slug" keyword argument here comes from the regex capture group in
# routing.py.

def connect_log(message, abcd, clear=False):
    group_id = "tailf" + abcd
    Group(group_id).add(message.reply_channel)
    try:
        group = Channelforlog.objects.get(channel_id=abcd)
        group.group_num = group.group_num + 1
        group.save()

        # for group in Channelforlog.objects.all():
        #     group.delete()IntegrityError
        # print u"已清空通道组数据表"
    except Channelforlog.DoesNotExist:

        try:
            if clear:
                Channelforlog.objects.create(channel_id=abcd, group_num=1, enforce=True)
            else:
                Channelforlog.objects.create(channel_id=abcd,group_num=1)
        except django.db.IntegrityError:  # channel_id 不唯一报错
            Group(group_id).send({
                "text": json.dumps({"line": '操作太快，服务器没反应过来'}),
            })
            return

        print u"开始连接websocket", group_id
        print "message.reply_channel:", message.reply_channel

        print u"开始打印日志"
        tailf = Tailflogoperate(abcd)
        ssh = tailf.execcmd(group_id)
        if ssh == None:
            Group(group_id).send({
                "text": json.dumps({"line": '主机连接失败socket.timeout'}),
            })
            group = Channelforlog.objects.get(channel_id=abcd)
            group.delete()
            return
        transport = ssh.get_transport()
        channel = transport.open_session()
        channel.get_pty()
        channel.exec_command('bash /tmp/' + group_id + '.sh')
        #channel.exec_command('docker exec -it 90ef10d8b52e tailf /cihi/logs/catalina.out')
        print u"准备 读取日志"
        while 1:
            if channel.exit_status_ready():
                print u"远程进程退出"
                break
            try:
                rl, _, _ = select.select([channel], [], [], 1)
                if len(rl) > 0:
                    recv = channel.recv(65536)
                    recv = cgi.escape(recv)
                    Group(group_id).send({
                        "text": json.dumps({"line": recv}),
                    })

            except Exception:  # KeyboardInterrupt
                print 'got ctrl+c'
                channel.send("\x03")  # 发送 ctrl+c
                channel.close()
                ssh.close()
                break

#@channel_session_user
def disconnect_log(message, abcd):

    group_id = "tailf" + abcd
    Group(group_id).discard(message.reply_channel)
    try:
        group = Channelforlog.objects.get(channel_id=abcd)
        group.group_num = group.group_num -1
        if group.group_num > 0:
            group.save()
            return
        else:
            group.delete()
    except Channelforlog.DoesNotExist:
        pass
    print u'最后当前websocket:',group_id
    #Group(group_id).discard(message.reply_channel)
    print "disconnect,message.reply_channel:", message.reply_channel
    ssh = Tailflogoperate(abcd)
    print "md5:", group_id
    returncode = ssh.killcmd(group_id)
    if returncode == 0:
        print u"停止tailf log 执行成功 returncode:", returncode
    else:
        print u"停止tailf log 执行失败 returncode:", returncode




#@channel_session_user_from_http
def save_post(message, abcd):
    """
    Saves vew post to the database.
    """
    group_id = "tailf" + abcd
    action = json.loads(message['text'])['action']
    if action == 'STOP':
        Group(group_id).discard(message.reply_channel)
    elif action == 'START':
        Group(group_id).add(message.reply_channel)
    elif action == 'CLEAR':
        try:
            group = Channelforlog.objects.get(channel_id=abcd)
        except Channelforlog.DoesNotExist:
            print u"清空通道组时，出错！"
            pass
        group.delete()
        print u"清空server_id:", action
        disconnect_log(message, abcd)
        connect_log(message, abcd, clear=True)


