# -*- coding:utf-8 -*-

from django import forms

class LoginForm(forms.Form):
	username = forms.CharField(max_length=50,label='用户名')
	password = forms.CharField(widget=forms.PasswordInput,label='密码')
	# something1 = forms.CharField(max_length=50,label='试试这是啥')