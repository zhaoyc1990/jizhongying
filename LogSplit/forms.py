# coding:utf-8
from django.forms import ModelForm
from LogSplit.models import LogSplit
from django import forms
#按指定时间之间截取
class CreateLogSplit(ModelForm):
	class Meta:
		model = LogSplit
		fields = ['server','starttime','stoptime','creatfilename']

#按指定最后多少行截取日志
class CreateLogSplitNext(ModelForm):
	number = forms.IntegerField(label='最后几行')
	class Meta:
		model = LogSplit
		fields = ['server','creatfilename']

#按最后多少分钟/小时/天截取日志
class CreateLogSplitTime(ModelForm):
	time_number = forms.IntegerField(label='最后多少时间')
	class Meta:
		model = LogSplit
		fields = ['server','creatfilename']
