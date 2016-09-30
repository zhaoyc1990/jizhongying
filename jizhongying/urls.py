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
urlpatterns = [
	url(r'^Operatefile/$', host_views.operatefile, name='operatefile'),
	url(r'^hostlist/$', host_views.hostlist, name='showhostlist'),
	url(r'^addhost/$', host_views.addhost, name='addhost'),
	url(r'^logsplit/$', logsplit_views.logsplit, name='logsplit'),
	url(r'^upload/$', logsplit_views.file_download, name = 'upload'),
    url(r'^$', logsplit_views.index, name='index'),
    url(r'^admin/', admin.site.urls),
]
