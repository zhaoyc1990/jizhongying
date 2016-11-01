# coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse
import os
# Create your views here.
from django.utils.datastructures import MultiValueDictKeyError


def server(request):
	
	
	return render(request, 'server.html', )
	
def addserver(request):
	if request.method == 'POST':
		#先定义一个字典包含上级页面所有name,以便遍历使用
		html_name = {
			'name_Zh':[], # 服务中文名
			'name_En':[],	#服务英文名
			'group':[],		#运行服务宿主主机所在组
			'host':[],		#运行服务宿主主机名
			'environment':[],	#运行环境选择
			'container':[],	#是否需要容器化
			'tag':[],			#环境版本如.java1.6/1.7/1.8
			'port':[],			#如需要需要容器，则开放端口号,list
			'gitsite':[],		#GIT版本控制地址
			'symbol':[],		#key与value 的赋值符号 :/=
			'filetype':[],		#配置文件类型(不代表文件后缀)	json/txt
			#'configure_key':[],	#配置文件 key
			#'configure_value':[],#配置文件 value
		}
		#遍历html_name 给addserver_from赋值
		for key in html_name:
			html_name[key] = request.POST.get(key,'')
			print(type(html_name[key]))
			print(key + ":" + html_name[key])
		#因为configure_key 和value 是配对的list 所以它俩单独遍历
		i = 0
		key_list = []
		value_list= []
		while True:
			i = i+1
			try:
				key_list.append(request.POST['configure_key'+ str(i)])
				value_list.append(request.POST['configure_value'+str(i)])
			except MultiValueDictKeyError:
				break
		print "key_list:" , key_list
		print "value_list" ,value_list
		#获取当前目录的上级目录
		rootpath = os.getcwd()#key与value 的赋值符号
		#所有管理git 的项目目录
		projectpath = os.path.normpath(rootpath + '/server/git')
		#切换工作目前，以执行git 操作
		#os.chdir(projectpath)
		return render(request, 'addserver.html', {'html_name': html_name} )
	else:
		return render(request, 'addserver.html', )
	
def version_switch(request):

	
	return render(request, 'server.html', )
	
def mobliemanager(request):


	#获取当前目录的上级目录
	rootpath = os.getcwd()
	#所有管理git 的项目目录
	projectpath = os.path.normpath(rootpath + '/git/MobileManager')
	#切换工作目前，以执行git 操作
	if os.path.exists(projectpath):
		#配置git 用户密码
		os.system('git config --global user.name root')
		os.system('git config --global user.email cihi@1415926')
		#is_succeed成功返回0
		is_succeed = os.system('git clone http://114.215.120.180:8907/Cihi/MobileManager.git')
		#如果没有成功下载代码，重试一次
		if is_succeed:
			os.system('git clone http://114.215.120.180:8907/Cihi/MobileManager.git')
		#如果两次均未成功，则返回出错信息
		if is_succeed:
			return render(request, 'server.html', {'message': '代码库未下载成功，请确认网络没有问题'})
	os.chdir(projectpath)
	# checkout "online" 取返回值是否等于0 来判断是否有这个分支，如有则删除，以chekcout -d <tag>
	is_succeed = os.system('git checkout online')
	if is_succeed:
		os.system('git checkout master')
		os.system('git branch -d online')
	#if
	# 切换分支+标签
	os.system('git checkout -b origin ' + version_no)
	
	return render(request, 'server.html',)
# def exec_git(cmdd):
	# is_succeed = os.system(cmd)
	# if not is_succeed:
		# return os.popen(cmd)
	# return 0