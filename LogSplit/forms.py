# coding:utf-8
from django.forms import ModelForm
from LogSplit.models import LogSplit
from django import forms
class CreateLogSplit(ModelForm):
	class Meta:
		model = LogSplit
		fields = ['server','starttime','stoptime','creatfilename']
		
# class CreateLogSplitNext(ModelForm):
	# number = forms.IntegerField(label='最后几行')
	# class Meta:
		# model = LogSplit
		# fields = ['server','creatfilename']