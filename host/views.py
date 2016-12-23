# coding:utf-8
import random

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .forms import AddHost
from .forms import Operatefile
from host.models import hostinfo, Group
from server.models import Server,Environment
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
	
#查看各分组主机状态 由这里可以进入各主机所运行的服务状态
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
		return JsonResponse({'message':'分组ID没传过来，别把它玩坏了'})
	elif group_id == '0':
		hostlist = hostinfo.objects.all()
	else:
		hostlist = hostinfo.objects.filter(group=group_id)
	listhost = {}
	if hostlist.exists():
		for host in hostlist:
			listhost.update(host.getid())
	else:
		return JsonResponse({'message': '没找到分组ID，别把它玩坏了'})
	return JsonResponse(listhost)

#显示指定主机各服务状态和可行操作
def gethostinfo(request):
    try:
        host_id = request.GET.get('hostid','')
        if host_id == '':
            return render(request, 'hostinfo.html', {'message': 'None', })
        else:
            #从DB里查找所有运行在host_id 里的服务
            server_query = Server.objects.values('id','name_Zh','name_En','port','curr_tag','server_status','container_id').filter(server_host=host_id)
            if server_query.exists():
                #查询的集合放到type be list to server_list
                server_list = []
                print u'不为空'
                for server in server_query:
                    server_list.append(server)
            else:
                return render(request, 'hostinfo.html', {'message': '该主机下没有服务', })
    except Exception , e:
        print u'出错了：' + e.__str__()
        return render(request, 'hostinfo.html', {'message': 'None', })
    print u'有返回'
    randomm =  random.randint(1, 100)
    return render(request, 'hostinfo.html', {'message': 'success','server_list':server_list,'randomm':randomm})
