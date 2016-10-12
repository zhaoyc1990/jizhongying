# coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse
import os
# Create your views here.
def server(request):
	
	
	return render(request, 'server.html', )
	
def addserver(request):
	#先定义一个字典包含上级页面所有name,以便遍历使用
	#获取当前目录的上级目录
	rootpath = os.getcwd()
	#所有管理git 的项目目录
	projectpath = os.path.normpath(rootpath + '/server/git')
	#切换工作目前，以执行git 操作
	#os.chdir(projectpath)
	
	
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