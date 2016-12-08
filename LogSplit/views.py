# coding:utf-8
import datetime
from django.shortcuts import render
from django.http import HttpResponse
from .forms import CreateLogSplit
from .forms import CreateLogSplitNext
from .forms import CreateLogSplitTime
from host.models import hostinfo
from .LogSplitt import LogSplit
from .models import servicename
from .LogSplitt import LogSplit
import time
import os
# Create your views here.
def index(request):
	return render(request, 'index.html')
	
#日志截取from:
def logsplit(request):
	# 当提交表单时
	if request.method == 'POST':
		linenum = request.POST.get('number','') # 最后几行条件
		time_num = request.POST.get('time_number','')#最后多少时间条件
		form1 = CreateLogSplit()
		form2 = CreateLogSplitNext()
		form3 = CreateLogSplitTime()
		if linenum:
			form = CreateLogSplitNext(request.POST)
			form2 = form
		elif time_num:
			form = CreateLogSplitTime(request.POST)
			form3 = form
		else:
			form = CreateLogSplit(request.POST) # form 包含提交的数据
			form1 = form
		log = form.save(commit=False)
		#servicenamelog = servicename.objects.get(id=int(request.POST.get('server')))
		#if form.is_valid():# 如果提交的数据合法
			#form.save()
		hostss = log.server.host
		hostdict = {'ip':hostss.ip, 'port':hostss.sshport, 'user':hostss.rootname, 'pswd':hostss.rootpassword}
		#先判断 是否需要计算开始和结束时间(比如：在按指定最后多少时间时)
		if time_num:
			log.stoptime = time.strftime("%Y-%m-%d %H:%M", time.localtime())
			time_term = request.POST.get('time_term','')
			time_num = int(time_num)
			if time_term == 'h': #按小时
				log.starttime = (datetime.datetime.now()-datetime.timedelta(hours=time_num)).strftime("%Y-%m-%d %H:%M")
			elif time_term == 'd':
				log.starttime = (datetime.datetime.now() - datetime.timedelta(days=time_num)).strftime("%Y-%m-%d %H:%M")
			elif time_term == 'm':
				log.starttime = (datetime.datetime.now() - datetime.timedelta(minutes=time_num)).strftime("%Y-%m-%d %H:%M")
		print u"开始时间:", log.starttime
		print u"结束时间:", log.stoptime
		# 从一对多关系数据库查询是否在容器里，而为容器端口赋值
		if log.server.timetype == "u":
			logstarttime = datetime_timestamp(log.starttime)
			logstoptime =  datetime_timestamp(log.stoptime)
		else:
			# "^" 正则行首的意思，增加sed 截取命中率
			logstarttime = "^" + quzore(log.starttime.replace("-", log.server.timetype).replace("T", " "))
			logstoptime =  "^" + quzore(log.stoptime.replace("-", log.server.timetype).replace("T", " "))
		#如截取后的文件 名没填写就保存当前时候为文件名
		if log.creatfilename == "": #如果表单里面没有指定文件名则按当前时间
			destfile = str(time.strftime("%m-%d-%H-%M")) + ".log"
		else:
			destfile = log.creatfilename
		#判断是否在容器里面，从而做不同的处理
		if log.server.is_container:
			container_port = log.server.port
			#是否需要交给跳板机操作
			if log.server.is_botnet:
				#从数据库获取跳板机信息，组装dict 
				forwarding_host = log.server.forwarding_host
				forwarding_hostdict = {'ip':forwarding_host.ip, 'port':forwarding_host.sshport, 'user':forwarding_host.rootname, 'pswd':forwarding_host.rootpassword}
				logss = LogSplit(hostdict, logstarttime, logstoptime, log.server.log_path, destfile, forwarding_hostdict, conport=log.server.port, linenum=linenum)
			else:
				logss = LogSplit(hostdict, logstarttime, logstoptime, log.server.log_path, destfile, conport=log.server.port, linenum=linenum)
		elif log.server.is_botnet:
			forwarding_host = log.server.forwarding_host
			forwarding_hostdict = {'ip':forwarding_host.ip, 'port':forwarding_host.sshport, 'user':forwarding_host.rootname, 'pswd':forwarding_host.rootpassword}
			container_port = None
			logss = LogSplit(hostdict, logstarttime, logstoptime, log.server.log_path, destfile, forwarding_hostdict, linenum=linenum)
		else:
			logss = LogSplit(hostdict, logstarttime, logstoptime, log.server.log_path, destfile, linenum=linenum)
		#执行远程操作,
		message = logss.ssh_download()
		#先判断信息中是否有文件名包含
		if destfile in message:
			destfile = message
			message = None
		#错误信息返回，显示在网页上
		if message != None:
			return render(request, 'logsplit.html', {'form': form1, 'form_next': form2, 'form_time': form3, 'message': message})
		filepath = "?filename=" + destfile

		return render(request, 'download.html', {'filepath': filepath,'filename':destfile })
		
	else:# 当正常访问时
		form = CreateLogSplit()
		form_next = CreateLogSplitNext()
		form_time = CreateLogSplitTime()
		#pass
	return render(request, 'logsplit.html', {'form': form, 'form_next': form_next, 'form_time':form_time})
	

#去时间戳后面的零
def quzore(s):
	s=str(s)
	if len(s) == 0: #在截取条件不是按时间截取的话那s的长度为零
		return ''
	while True:
		if s[-1] == "0":
			s = s[0:-1]
		else:
			break
	return s

	#返回标准时间2016/08/08 08:08 的时间戳
def datetime_timestamp(dt):
	dt = dt.replace("T", " ")
	#dt为字符串
	#中间过程，一般都需要将字符串转化为时间数组
	time.strptime(dt, '%Y-%m-%d %H:%M')
	## time.struct_time(tm_year=2012, tm_mon=3, tm_mday=28, tm_hour=6, tm_min=53, tm_sec=40, tm_wday=2, tm_yday=88, tm_isdst=-1)
	#将"2012-03-28 06:53:40"转化为时间戳
	s = time.mktime(time.strptime(dt, '%Y-%m-%d %H:%M'))
	strr = quzore(int(s))
	# 返回的时候 加上"-- 增加sed 命中率,仅针对时间戳"
	return "-- " + strr

	
#文件下载
from django.http import StreamingHttpResponse 
def file_download(request):
	# do something...

	def file_iterator(file_name, chunk_size=512):
			with open(file_name, 'rb') as f:
				while True:
					c = f.read(chunk_size)
					if c:
						yield c
					else:
						break
	destfile = request.GET['filename']
	the_file_name = os.path.normpath(os.path.abspath("./upload/") + "/" + destfile)
	response = StreamingHttpResponse(file_iterator(str(the_file_name)))
	response['Content-Type'] = 'application/octet-stream'
	response['Content-Disposition'] = 'attachment;filename="{0}"'.format(destfile)
	return response