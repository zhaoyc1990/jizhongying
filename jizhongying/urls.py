# coding: utf-8
"""jizhongying URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
import LogSplit.views as logsplit_views
import host.views as host_views
import server.views as server_views
urlpatterns = [
    url(r'^jsontest/$', server_views.jsontest, name='jsontest'),
	url(r'^version_switch/$', server_views.version_switch, name='version_switch'),
	url(r'^addserver/$', server_views.addserver, name='addserver'),
	url(r'^server/$', server_views.server, name='server'),
	url(r'^server/deploy/$', server_views.deploy, name='deploy'),
    url(r'^server/more/([a-z+]+)/(\d+)/(\d+)/$', server_views.rst_container, name='more_operat'),
    url(r'^server/rm_server/$', server_views.rm_server, name='rm_server'),
	url(r'^server/getservertags/(\d+)/$', server_views.getservertags, name='server_tags'), #获取代码版本号列表
	url(r'^Operatefile/$', host_views.operatefile, name='operatefile'),
	url(r'^hostlist/$', host_views.hostlist, name='showhostlist'),
	url(r'^hostlist/getJsGroupinfo/$', host_views.getJsGroupinfo, name='getJsGroupinfo'),
	url(r'^hostlist/gethostinfo/$', host_views.gethostinfo,name='gethostinfo'),
	url(r'^addhost/$', host_views.addhost, name='addhost'),							#添加主机
	url(r'^logsplit/$', logsplit_views.logsplit, name='logsplit'),						#日志截取
	url(u'^addserver/startinit/$' ,server_views.startinit, name='startinit'),			#后台初始化docker
	url(r'^addserver/Jquery_get_message/(\d+)/$', server_views.Jquery_get_message, name='Jquery_get_message'),
	url(r'^addserver/getenv_tags/$', server_views.getMeEnvTags, name='getenv_tags'),
	url(r'^addserver/gethosts/$', server_views.getMeGroupUserJson, name='gethosts'),#jquery 动态加载主机
	url(r'^upload/$', logsplit_views.file_download, name = 'upload'),
    url(r'^$', logsplit_views.index, name='index'),
    url(r'^admin/', admin.site.urls),
]
