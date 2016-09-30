from django.forms import ModelForm
from LogSplit.models import LogSplit
from django import forms
class CreateLogSplit(ModelForm):
	class Meta:
		model = LogSplit
		fields = ['server','starttime','stoptime','creatfilename']