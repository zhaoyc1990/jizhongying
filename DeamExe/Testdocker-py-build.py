# coding: utf-8
#!/bin/bin/env python
# import sys
# from docker import Client
# from io import BytesIO
# import tarfile, os
# if __name__ == '__main__':
    # image = '192.168.2.246:5000/weserver:1.0'
    # tag = 'latest'
    # dockerfile = '''
    # # Zhaoyc
    # FROM ''' + image + ':' + tag + '''
    # CMD tail -f /etc/passwd
    # '''
    # f = BytesIO(dockerfile.encode('utf-8'))
    # cli = Client(base_url='tcp://192.168.239.128:6732')
    # response = [line for line in cli.build(
    #     fileobj=f, rm=True, tag='192.168.2.246:5000/webserver:1.0'
    # )]
    # print response
    #################################################
    # image = '192.168.2.246:5000/webserver:1.0'
    # cli = Client(base_url='tcp://192.168.239.128:6732')
    # host_confi = cli.create_host_config(restart_policy={'Name':'always'},port_bindings={2222:2222,4040:4343,8089:8092})
    #
    # responsed = cli.create_container(image=image,host_config=host_confi,environment={"TZ":"Asia/Shanghai"},
    #                                   ports=[2222,4040,8089])
    # print responsed
    # response = cli.start(container=responsed['Id'])
    # print response
    ###############################################
    # def reverse(pp):
    #     if type(pp) is dict:
    #         if pp != {}:
    #             for key, value in pp.items():
    #                 pp[value] = key
    #     return pp
    # dd = {444:333,5555:6666,'dddd':'ffff',44444:4444}
    # print reverse(dd)
    #
    ################################################



    # def mak_tar(foldername, dest_folder, compression='gz'):
    #     if compression:
    #         dest_ext = '.' + compression
    #     else:
    #         dest_ext = ''
    #     arcname = os.path.basename(foldername)
    #     dest_name = '%s.tar%s' % (arcname, dest_ext)
    #     dest_path = os.path.join(dest_folder, dest_name)
    #     if compression:
    #         dest_cmp = ':' + compression
    #     else:
    #         dest_com = ''
    #     out = tarfile.TarFile.open(dest_path, 'w' + dest_cmp)
    #     out.add(foldername, arcname)
    #     out.close()
    #     return dest_path
    #
    #
    # curr_dir = os.path.split(os.path.realpath(__file__))[0]
    # # git仓库下载到本地哪个目录
    # # gitpath = os.path.normpath(os.getcwd() + '/git')
    # wocao =  os.path.split(curr_dir)
    # print wocao[0]
    # # gitpath = os.path.normpath(wocao[0] + '/git')
    # gitpath = os.path.normpath(wocao[0])
    # os.chdir(gitpath)
    #
    # print mak_tar('git/ownscript','upload')
    # # print mak_tar(r'D:\YYGameBox', r'D:\123')

    ########################################################################################################
# from bottle import request, Bottle, abort
# from geventwebsocket import WebSocketError
# from gevent.pywsgi import WSGIServer
# from geventwebsocket.handler import WebSocketHandler
# from websocket import create_connection
# app = Bottle()
# users = set()
# @app.get('/websocket/')
# def handle_websocket():
#     wsock = request.environ.get('wsgi.websocket')
#     users.add(wsock)
#     if not wsock:
#         abort(400, 'Expected WebSocket request.')
#     while True:
#         try:
#             message = wsock.receive()
#         except WebSocketError:
#             break
#         print u"现有连接用户：%s" % (len(users))
#         if message:
#             for user in users:
#                 try:
#                     user.send(message)
#                 except WebSocketError:
#                     print u'某用户已断开连接'
#     # 如果有客户端断开，则删除这个断开的websocket
#     users.remove(wsock)
# server = WSGIServer(("0.0.0.0", 8000), app, handler_class=WebSocketHandler)
# server.serve_forever()



#########################################################
import os
import paramiko
f = open('wodd'+".sh",'w+')
f.write("wocao")
f.seek(0)  #因为文件写入字符串后，文件指针在最后面了， 所以需要seek 0 把指针放在文件第一个字符前
t = paramiko.Transport(('192.168.2.84',22))
t.connect(username='root', password='chang')
sftp = paramiko.SFTPClient.from_transport(t)
try:
	sftp.put('wodd.sh', os.path.join('/tmp/', 'wodd' + '.sh'))
except IOError, e:
	sftp.putfo(f, os.path.join('/tmp/', 'wodd' + '.sh'))
	raise IOError(e)
finally:
	del(f)
	t.close()
