# coding=utf-8

from django.views.generic import TemplateView


class Index(TemplateView):
    template_name = 'ate_tasks/index.html'
