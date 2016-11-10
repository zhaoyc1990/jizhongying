# coding:utf-8
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone as timezone
# Create your models here.
class Group_script(models.Model):
	group_name = models.CharField(u'功能类别', max_length=50)
	
	def __unicode__(self):
		return self.group_name

class Script(models.Model):
	group = models.ForeignKey(Group_script, related_name='groupscrit_set')
	filename = models.CharField(u'脚本文件名',max_length=60)
	filepath = models.FileField(u'脚本路径',upload_to='upload/')
	description = models.TextField(u'功能简述')
	modified = models.DateTimeField(u'最后修改日期', auto_now = True)
	createdate = models.DateTimeField(u'创建/添加日期', default = timezone.now)
	def __unicode__(self):
		return self.filename

class Group(models.Model):
	group_name = models.CharField(u'组名', max_length=50, default=u'未分组')
	docker_registry = models.CharField(u'docker仓库地址及端口',max_length=50, default=u'空')
	def __unicode__(self):
		return self.group_name
	def getall(self):
		return {str(self.id): self.group_name}
		
class hostinfo(models.Model):
	group = models.ForeignKey(Group, related_name='group_set',blank=False, default='未分组')
	name = models.CharField(u'主机名', max_length=30)
	ip = models.GenericIPAddressField(u'ip 地址')
	rootname = models.CharField(u'管理员用户名', max_length=50)
	rootpassword = models.CharField(u'密码', max_length=30)
	sshport = models.IntegerField(u'SSH端口')
	docker_remote_api_port = models.IntegerField(u'docker远程API端口', blank=True, null=True)
	host_status = models.BooleanField(u'主机运行状态', default=True)
	description = models.TextField(u'简述信息', default=u'无')
	spare = models.CharField(u'备用扩展字段', max_length=30, blank=True)
	script = models.ForeignKey(Script, blank=True, null=True)
	modified = models.DateTimeField(u'最后修改日期', auto_now = True)
	createdate = models.DateTimeField(u'创建/添加日期', default = timezone.now)
	def __unicode__(self):
		return self.name
	def getid(self):
		return {str(self.id): self.name}

