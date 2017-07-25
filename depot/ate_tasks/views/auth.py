# coding=utf-8
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.views.generic import FormView, RedirectView

import ate_tasks.forms as forms


class LoginView(FormView):
    form_class = forms.LoginForm
    template_name = 'ate_tasks/auth/login.html'

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('ate_tasks:index')
        else:
            messages.error(request, '登录失败，请核对信息后重试')
            return render(request, 'ate_tasks/auth/login.html', self.get_context_data())


class LogoutView(RedirectView):
    pattern_name = 'ate_tasks:index'

    def get_redirect_url(self, *args, **kwargs):
        logout(self.request)
        return super(LogoutView, self).get_redirect_url(*args, **kwargs)
