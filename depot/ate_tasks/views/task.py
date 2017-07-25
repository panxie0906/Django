# coding=utf-8
import zerorpc
from django.conf import settings
from django.db.models import ObjectDoesNotExist
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
from django.views.generic import DetailView, ListView
from openpyxl import Workbook
from openpyxl.writer.excel import save_virtual_workbook

import ate_tasks.models as models

ENGINE_ADDRESS = settings.TEST_ENGINE_SETTINGS['ADDRESS']
JSON_DUMPS_PARAMS = settings.TEST_ENGINE_SETTINGS['JSON_DUMPS_PARAMS']


class ShowRunnerView(ListView):
    template_name = 'ate_tasks/execute/runner_list.html'
    model = models.TaskInstance
    paginate_by = 15

    def get_queryset(self):
        return models.TaskInstance.objects.order_by('created')


class TaskRunnerView(DetailView):
    model = models.TaskInstance
    template_name = 'ate_tasks/execute/runner.html'

    def get_context_data(self, **kwargs):
        task_instance_uuid = self.object.uuid
        context = super(TaskRunnerView, self).get_context_data(**kwargs)
        context['task_instance_uuid'] = task_instance_uuid
        context['index_url'] = "ate_tasks:execute-task-instance-index"
        context['verbose_name'] = '测试任务实例'
        context['steps'] = self.object.task.steps.all().order_by('order')
        context['flow_chart_string'] = self.object.flow_chart_string
        return context


@require_http_methods(['GET', ])
def suspend_task(_, pk):
    submit_result = {}
    try:
        rpc_client = zerorpc.Client()
        rpc_client.connect(ENGINE_ADDRESS)
        task_instance = models.TaskInstance.objects.get(id=pk)
        result = rpc_client.suspend_task(task_instance.uuid.__str__())
        if result:
            submit_result['result'] = True
            submit_result['detail'] = '任务实例{0}停止成功'.format(pk)
        else:
            submit_result['result'] = False
            submit_result['detail'] = '任务实例{0}停止失败'.format(pk)
    except ObjectDoesNotExist:
        submit_result['result'] = False
        submit_result['detail'] = "任务实例{0}不存在".format(pk)
    except BaseException as e:
        submit_result['result'] = False
        submit_result['detail'] = "发生异常{0}".format(e.__traceback__)
    return JsonResponse(submit_result, json_dumps_params={'ensure_ascii': False})


@require_http_methods(['GET', ])
def run_task_instance(_, pk):
    submit_result = {}
    try:
        rpc_client = zerorpc.Client()
        rpc_client.connect(ENGINE_ADDRESS)
        task_instance = models.TaskInstance.objects.get(id=pk)
        task_instance.result = '[]'
        task_instance.detail = '{}'
        task_instance.save()
        task = task_instance.task
        test_items = [(step.__str__(), step.code, step.parameters) for step in
                      task.steps.order_by('order')]
        result = rpc_client.execute(task_instance.uuid.__str__(), task.name, test_items)
        if result:
            submit_result['result'] = True
            submit_result['detail'] = '任务实例{0}运行成功'.format(pk)
        else:
            submit_result['result'] = False
            submit_result['detail'] = '任务实例{0}运行失败'.format(pk)
    except ObjectDoesNotExist:
        submit_result['result'] = False
        submit_result['detail'] = "任务实例{0}不存在".format(pk)
    except BaseException as e:
        submit_result['result'] = False
        submit_result['detail'] = "发生异常{0}".format(e.__traceback__)
    return JsonResponse(submit_result, json_dumps_params={'ensure_ascii': False})


def get_instance_result(_, pk):
    instance = get_object_or_404(models.TaskInstance, id=int(pk))
    records = instance.clean_records
    excel_data = [['测试项名称', '测试结果', '备注']]
    for record in records:
        excel_data.append([record['name'], record['pass'], record['detail']])
    wb = Workbook(write_only=True)
    ws = wb.create_sheet()
    for line in excel_data:
        ws.append(line)
    response = HttpResponse(save_virtual_workbook(wb), content_type='application/octet-stream')
    response['Content-Disposition'] = 'attachment; filename={0}.xls'.format(instance.uuid)
    return response
