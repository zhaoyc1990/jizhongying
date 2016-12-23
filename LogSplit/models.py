# coding:utf-8
from __future__ import unicode_literals

from django.db import models
from host.models import hostinfo
from django.utils import timezone as timezone
from server.models import Server
# Create your models here.is_container
class servicename(models.Model):
	host = models.ForeignKey( hostinfo)
	name = models.CharField(u'服务名', max_length=50)
	is_container = models.BooleanField(u'服务是否在容器里', blank=True, default=True)
	is_botnet = models.BooleanField(u'服务是否需要跳板机操作', default=False)
	forwarding_host=models.ForeignKey(hostinfo, related_name='forwarding_host_set',verbose_name='跳板主机', blank=True, null=True)   #后续要把这个字段删除没用了
	server = models.ForeignKey(Server, verbose_name='关联服务', blank=True, null=True)
	port = models.IntegerField(u'服务端口', blank=True, null=True)
	timetype = models.CharField(u'时间格式分割符', default='-', max_length=2)  #'-' 代表 2000-00-00 00:00:00 'u':unix 时间戳 'e':Thu Apr  7 10:05:21 2016
	log_path = models.CharField(u'日志路径',max_length=100)
	modified = models.DateTimeField(u'最后修改日期', auto_now=True)
	createdate = models.DateTimeField(u'创建/添加日期', default=timezone.now)
	
	def __unicode__(self):
		return self.name
	def getid(self):
		return self.id
	def getdict(self):
		return {'id':self.id, 'name':self.name}

class LogSplit(models.Model):
	#host = models.ForeignKey(hostinfo, related_name='host_set')
	server = models.ForeignKey(servicename, related_name='servicename_set', blank=True, null=True)
	starttime = models.CharField(u'要截取的开始时间', max_length=30)
	stoptime = models.CharField(u'要截取的截止时间', max_length=30)
	linenum	= models.IntegerField(u'最后多少行',blank=True, null=True)
	logfilename = models.CharField(u'日志文件名(默认console.log)', max_length=60, default='console.log', blank=True, null=True)
	creatfilename = models.CharField(u'要生成的文件名(默认当前时间)',max_length=60, blank=True, null=True)
	createtime = models.DateTimeField(u'创建/添加日期', default = timezone.now)

	def __unicode__(self):
		return self.creatfilename
