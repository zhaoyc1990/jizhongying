# coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .forms import AddHost
from .forms import Operatefile
from host.models import hostinfo, Group
from django.views.decorators.csrf import csrf_exempt
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
	grouplist = Group.objects.all()
	listgroup = {}
	if grouplist.exists():
		for group in grouplist:
			listgroup.update(group.getall())
	else:
		print u"分组为空"
	hlist = hostinfo.objects.all()
	listhost = {}
	if hlist.exists():
		for host in hlist:
			listhost.update(host.getid())
	print hlist
	return render(request, 'hostlist.html', {'hostlist': listhost,'grouplist':listgroup})

#Jquery 过来动态调分组中的主机列表
@csrf_exempt
def getJsGroupinfo(request):
	group_id= request.GET.get('groupid','')
	if group_id == '':
		return JsonResponse({'message':'分组ID没传过来，别把它玩错了'})
	elif group_id == '0':
		hostlist = hostinfo.objects.all()
	else:
		hostlist = hostinfo.objects.filter(group=group_id)
	listhost = {}
	if hostlist.exists():
		for host in hostlist:
			listhost.update(host.getid())
	else:
		return JsonResponse({'message': '没找到分组ID，别把它玩错了'})
	return JsonResponse(listhost)


def gethostinfo(request):
	return render(request, 'hostinfo.html', {'message': '...', })