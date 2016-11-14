# coding:utf-8
import os
from multiprocessing import Process, Queue
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.datastructures import MultiValueDictKeyError
from django.views.decorators.csrf import csrf_exempt
from docker import Client
import requests
from .models import Server
from . import Gitopera
from server.models import Environment, HttpChannel, Server
from host.models import Group, hostinfo

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
			print(type(html_name[key]))
			print(key + ":" + html_name[key])

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
		i = 0
		key_list = []
		value_list = []
		while True:
			i = i + 1
			try:
				if request.POST['configure_key' + str(i)] == u'':
					break
				key_list.append(request.POST['configure_key' + str(i)])
				value_list.append(request.POST['configure_value' + str(i)])
			except MultiValueDictKeyError:
				break
		print "key_list:", key_list
		print "value_list", value_list
		# 把key, value list 放在html_name里面
		html_name['configure_key'] = key_list
		html_name['configure_value'] = value_list

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
		return render(request, 'addserver.html', {'html_name': html_name, 'message':message,'serverid':serverid})
	else:
		html_name['group'] = group_dict
		html_name['environment'] = environment
		return render(request, 'addserver.html', {'html_name': html_name, 'nothing':'---------'})

def gitclone(q,gitsite):
	HttpChannel.objects.create(message='Begining git download...')
	git = Gitopera(gitsite)
	returnCode = git.clone()
	if returnCode == 0:
		HttpChannel.objects.create(message='git download success!')
	else:
		HttpChannel.objects.create(message='git download fail!!!')

from requests.exceptions import ConnectionError
import json
#host 宿主机id			is_container  boolean 是否容器化
#environment			镜像地址比如 192.168.2.246:5000/busybox
#env_tag				镜像表签 latest	1.0
def dockerinit(host, is_container, environment, env_tag):
	HttpChannel.objects.create(message='Begining images for docker download...')
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
		for line in cli.pull(image['image'],tag=env_tag,stream=True):
			print type(line)
			print line
			HttpChannel.objects.create(message=json.dumps(json.loads(line), indent=4))

@csrf_exempt
def startinit(request):
	message = {'message':''}
	html_name = {
		'id':'',
		'host':'',
		'container':'',
		'environment':'',
		'tag':'',
		'gitsite':''
	}
	for key in html_name:
		html_name[key] = request.GET.get(key, '')
		print key + ":get:" + html_name[key]
		if html_name[key] == '':
			return JsonResponse({'message':'Error:'+ key + ' not Null'})

	print u"开始初始化"
	# 开启三个进程同时进行
	# 1.git 仓库初始化
	# 2,如果需要有容器化会从该组的仓库地址获取镜像到宿主机
	# 3.实时获取前面两个进程打印回来的信息

	# pgit = Process(target=gitclone, args=(q,html_name['gitsite']))
	print "Start...."
	try:
		dockerinit(html_name['host'], html_name['container'], html_name['environment'], html_name['tag'])
		# pdocker = Process(target=dockerinit,
		# 				  args=(q, html_name['host'], html_name['container'], html_name['environment'], html_name['tag']))
		# receive_put = Process(target=getprocessinfo, args=(q))
		# pgit.start()
		# pdocker.start()
		# receive_put.start()
		# pdocker.join()
		# receive_put.terminate()
		message['message'] = 'success'
		HttpChannel.objects.create(message='success')
	except ConnectionError ,ee:
		print u"连接宿主机超时"
		HttpChannel.objects.create(message=u'连接宿主机错误003')
		print ee
		print html_name['id']
		print type(html_name['id'])
		bab_server = Server.objects.filter(id=int(html_name['id']))
		bab_server.delete()
		HttpChannel.objects.create(message='Error')
		message['Error'] = 'Error'
	return JsonResponse(message)

# http jquery 过来调 用的函数
@csrf_exempt
def Jquery_get_message(request):
	message = HttpChannel.objects.filter(take_out=False)
	p = {}
	if message.exists():
		for mess in message:
			p.update(mess.getmessage())
			mess.take_out = True
			mess.save()
	else:
		print u"初始化镜像和代码库过程：暂无新消息01"
		return JsonResponse({'message':'>>>'})
	return JsonResponse(p)

def version_switch(request):

	
	return render(request, 'server.html', )




# def exec_git(cmdd):
	# is_succeed = os.system(cmd)
	# if not is_succeed:
		# return os.popen(cmd)
	# return 0

# 取出POST页面选中的select type(dict)
def getmechecked(checked_dict, html_name_key):

	html_name_checked = {}  # 临时存放被选中的组名信息
	group_id = str(html_name_key)
	html_name_checked[group_id] = checked_dict[group_id]
	return html_name_checked

#从数据库取出指定组ID的主机type(dict)
def getMeGroupUser(id):
    pp = {}
    for host in hostinfo.objects.filter(group=id):
        pp.update(host.getid())
    return pp


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