# -*- coding:utf-8 -*-

from django.contrib.auth import authenticate,login,logout
from django.shortcuts import redirect,render
from django.views.generic import FormView,RedirectView
from django.contrib import messages


import polls.forms as forms

class LoginView(FormView):
	form_class = forms.LoginForm
	template_name = 'polls/auth/login.html'
	
	def post(self,request,*args,**kwargs):
		username = request.POST['username']
		passward = request.POST['passward']
		user = authenticate(request,username=username,password=password)
		
		if user is not None:
			login(request,user)
			return redirect('polls:time')
		else:
			messages.error(request,u'登录失败，请核定后重试')
			return render(request,'polls/auth/login.html')
		
class LogoutView(FormView):
	pattern_name = 'polls:time'
	
	def get_redirect_url(self,*args,**kwargs):
		logout(self.request)
		return super(LogoutView,self).get_redirect_url(*args,**kwargs)
