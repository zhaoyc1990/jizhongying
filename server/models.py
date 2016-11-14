# coding: utf-8
from __future__ import unicode_literals
from host.models import hostinfo
from host.models import Group
from django.db import models
from django.utils import timezone as timezone
# Create your models here.
class Environment(models.Model):
    env_name = models.CharField(u'环境名', max_length=50)
    env_tag = models.CharField(u'环境版本', max_length=50)
    is_image = models.BooleanField(u'是否是镜像', default=False)
    image = models.CharField(u'镜像存放地址', max_length=80,blank=True,null=True)
    filepath = models.CharField(u'环境所需文件地址（相对网站根目录）', max_length=100,blank=True,null=True)
    env_group = models.ForeignKey(Group, related_name='env_group',blank=True,null=True)
    env_status = models.BooleanField(u'镜像是否还在仓库里面', default=True)
    modified = models.DateTimeField(u'最后修改日期', auto_now=True)
    createdate = models.DateTimeField(u'创建/添加日期', default=timezone.now)
    def __unicode__(self):
        return self.env_name
    def getIdAndName(self):
        return {self.id:self.env_name}
    #返回一个tags列表
    def gettags(self):
        tags = []
        for tag in self.env_tag.split(','):
            tags.append(tag.strip())
        return tags


class Server(models.Model):
    name_Zh = models.CharField(u'服务中文名', max_length=50, blank=True, null=True)
    name_En = models.CharField(u'服务英文名', max_length=50)
    server_host =    models.ForeignKey(hostinfo,related_name='host_pid',)
    is_container = models.BooleanField(u'服务是否在容器里',default=False)
    server_environment = models.ForeignKey(Environment,related_name='environment_id',blank=True, null=True) #环境 pid
    port = models.CharField(u'服务端口', max_length=50, blank=True, null=True)
    gitsite = models.CharField(u'GIT仓库地址', max_length=80,blank=True,null=True)
    curr_tag = models.CharField(u'当前代码版本号', max_length=30, blank=True,null=True)  #代码当前版本号
    curr_env_tag = models.CharField(u'当前环境版本号', max_length=30, blank=True, null=True)
    container_id = models.CharField(u'容器ID', max_length=50, blank=True,null=True)
    server_status = models.BooleanField(u'容器状态', default=True)
    modified = models.DateTimeField(u'最后修改日期', auto_now=True)
    createdate = models.DateTimeField(u'创建/添加日期', default=timezone.now)
    def __unicode__(self):
        return self.name_Zh
    def gettag(self):
        return self.curr_tag
    def getserver_status(self):
        return self.server_status

class ConfigureFile(models.Model):
    conf_server = models.ForeignKey(Server, related_name='conf_for_server')
    conf_group =  models.ForeignKey(Group, related_name='conf_for_group')
    conf_context = models.TextField(u'配置文件内容',blank=True, null=True)
    is_download = models.BooleanField(u'更改后是否下载',default=False)
    modified = models.DateTimeField(u'最后修改日期', auto_now=True)
    createdate = models.DateTimeField(u'创建/添加日期', default=timezone.now)

    def __unicode__(self):
        return self.modified

class HttpChannel(models.Model):
    message = models.TextField(u'message', blank=True, null=True)
    take_out = models.BooleanField(u'是否取走消息', default=False)

    def __unicode__(self):
        return self.message
    def getmessage(self):
        if self.message == None:
            return None
        print self.message
        return {self.id: self.message}