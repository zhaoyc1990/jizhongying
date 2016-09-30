# coding:utf-8
from __future__ import unicode_literals

from django.db import models
from host.models import hostinfo
from django.utils import timezone as timezone
# Create your models here.is_container
class servicename(models.Model):
	host = models.ForeignKey( hostinfo)
	name = models.CharField(u'服务名', max_length=50)
	is_container = models.BooleanField(u'服务是否在容器里')
	is_botnet = models.BooleanField(u'服务是否需要跳板机操作', default=False)
	forwarding_host=models.ForeignKey(hostinfo, related_name='forwarding_host_set', blank=True, null=True)
	port = models.IntegerField(u'服务端口', blank=True, null=True)
	timetype = models.CharField(u'时间格式分割符', default='-', max_length=2)
	log_path = models.CharField(u'日志路径',max_length=100)
	
	def __unicode__(self):
		return self.name

class LogSplit(models.Model):
	#host = models.ForeignKey(hostinfo, related_name='host_set')
	server = models.ForeignKey(servicename, related_name='servicename_set', blank=True, null=True)
	starttime = models.CharField(u'要截取的开始时间', max_length=30)
	stoptime = models.CharField(u'要截取的截止时间', max_length=30)
	logfilename = models.CharField(u'日志文件名(默认console.log)', max_length=60, default='console.log', blank=True, null=True)
	creatfilename = models.CharField(u'要生成的文件名(默认当前时间)',max_length=60, blank=True, null=True)
	createtime = models.DateTimeField(u'创建/添加日期', default = timezone.now)

	def __unicode__(self):
		return self.creatfilename
		
