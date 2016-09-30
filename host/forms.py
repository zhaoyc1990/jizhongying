# coding=utf-8
from django.forms import ModelForm
from host.models import hostinfo, Group
from django import forms
class AddHost(ModelForm):
	rootpassword = forms.CharField(widget=forms.PasswordInput())
	class Meta:
		model = hostinfo
		fields = ['group', 'name', 'ip', 'sshport', 'rootname', 'rootpassword', 'description']

class Operatefile(forms.Form):
	
	hostname = forms.ChoiceField(label='主机名',initial={'sdf':'sdfd', 'sddd':'fffff'})
	a = forms.IntegerField()
	b = forms.IntegerField()
	