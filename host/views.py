# coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse
from .forms import AddHost
from .forms import Operatefile
from host.models import hostinfo
# Create your views here.
def addhost(request):
	# 当提交表单时
	if request.method == 'POST':
		form = AddHost(request.POST) # form 包含提交的数据
		
		if form.is_valid():# 如果提交的数据合法
			form.save()
			return render(request, 'hostlist.html', {'form': form})
	 
	else:# 当正常访问时
		form = AddHost()
	return render(request, 'addhost.html', {'form': form})

#上传/下载文件from:
def operatefile(request):
	if request.method == 'POST':
		form = Operatefile(request.POST)
		
		if form.is_valid():
			a = form.cleaned_data['a']
			b = form.cleaned_data['b']
			return HttpResponse(str(int(a) + int(b)))
	else:
		form = Operatefile()
		# group = form.get['group']
		# print group
		#hostnames = hostinfo.objects.filter()
	return render(request, 'operate_file.html', {'form': form})
	
	
def hostlist(request):
	hlist = hostinfo.objects.all()
	print hlist
	return render(request, 'hostlist.html', {'hostlist': hlist})