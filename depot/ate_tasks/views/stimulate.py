# coding=utf-8
from django.http import JsonResponse
from django.views.generic.base import TemplateView, View

from .base import BaseTool


class StimulateIndex(TemplateView):
    template_name = 'ate_tasks/stimulate/index.html'

    @BaseTool.context_add_simple_icd_tree
    def get_context_data(self, **kwargs):
        context = super(StimulateIndex, self).get_context_data(**kwargs)
        return context


class StimulateSingleMessage(View):
    """执行单条激励，返回激励结果"""

    @staticmethod
    def post(request):
        result = {'result': True, 'data': dict(request.POST)}
        return JsonResponse(result, json_dumps_params={'ensure_ascii': False})
