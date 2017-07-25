# coding=utf-8
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, RedirectView, View

import ate_tasks.models as models
from .base import BaseTool


class NewMonitorView(RedirectView):
    pattern_name = 'ate_tasks:monitor-detail'

    def get_redirect_url(self, *args, **kwargs):
        monitor = models.Monitor.objects.create()
        kwargs['pk'] = monitor.id
        return super(NewMonitorView, self).get_redirect_url(*args, **kwargs)


class MonitorDetailView(DetailView):
    model = models.Monitor
    template_name = 'ate_tasks/monitor/monitor_detail.html'



    @BaseTool.add_rules_to_simple_icd_tree
    @BaseTool.context_add_simple_icd_tree
    def get_context_data(self, **kwargs):
        context = super(MonitorDetailView, self).get_context_data(**kwargs)
        return context


class SetMonitorFilterRule(View):
    @staticmethod
    def post(request, pk):
        monitor = get_object_or_404(models.Monitor, pk=pk)
        monitor.rules = request.POST.get('rules', '')
        monitor.save()
        return JsonResponse({'result': 'success'}, json_dumps_params={'ensure_ascii': False, 'indent': 4}, safe=False)
