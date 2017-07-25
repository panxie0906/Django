# coding=utf-8
import json

from django.contrib import messages as message_framework
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import (DeleteView, DetailView, FormView, ListView,
                                  View)
from json2html import json2html
from lxml import etree
from lxml.etree import XMLSyntaxError

import ate_tasks.models as models
from ate_tasks.forms import IcdUploadForm
from .base import BaseTool


class UploadIcdFormView(FormView):
    template_name = 'ate_tasks/icd/upload_file.html'
    form_class = IcdUploadForm
    success_url = reverse_lazy('ate_tasks:icd-project-list')
    message_attrs_dict = {
        'RS422': ['name', 'mode', 'period', 'sour', 'dest', 'length', 'id'],
        '1553B': ['name', 'mode', 'length', 'id']
    }

    @staticmethod
    def dumps(content):
        return json.dumps(content, ensure_ascii=False, indent=4)

    def __init__(self):
        super(UploadIcdFormView, self).__init__()
        self._project_attrs = ['name', 'version', 'id']
        self._product_attrs = ['name', 'version', 'id']
        self._bus_attrs = ['type']
        self._signal_attrs = ['name', 'length', 'start', 'end']
        self._domain_attrs = ['name', 'type', 'startbits', 'endbits', 'remark']

    def _parse(self, bus, product_object):
        bus_type = bus.get('type')
        message_attrs = self.message_attrs_dict.get(bus_type, [])
        messages = bus.xpath(BaseTool.xpath_expression_generator('Message', message_attrs))
        for message in messages:
            message_object, _ = models.IcdMessage.objects.update_or_create(message_id=message.get('id'),
                                                                           defaults={
                                                                               'name': message.get('name'),
                                                                               'bus': bus_type,
                                                                               'icd_product': product_object,
                                                                               'attrs': self.dumps(dict(message.attrib))
                                                                           })
            signals = message.xpath(BaseTool.xpath_expression_generator('Signal', self._signal_attrs))
            for signal in signals:
                signal_object, _ = models.IcdSignal.objects.update_or_create(name=signal.get('name'),
                                                                             message=message_object,
                                                                             defaults={
                                                                                 'length': signal.get('length'),
                                                                                 'start': signal.get('start'),
                                                                                 'end': signal.get('end'),
                                                                                 'attrs': self.dumps(
                                                                                     dict(signal.attrib))
                                                                             })
                domains = signal.xpath(BaseTool.xpath_expression_generator('Domain', self._domain_attrs))
                for domain in domains:
                    domain_project, _ = models.IcdDomain.objects.update_or_create(name=domain.get('name'),
                                                                                  signal=signal_object,
                                                                                  defaults={
                                                                                      'domain_type': domain.get(
                                                                                          'type'),
                                                                                      'start_bits': domain.get(
                                                                                          'startbits'),
                                                                                      'end_bits': domain.get(
                                                                                          'endbits'),
                                                                                      'remark': domain.get(
                                                                                          'remark'),
                                                                                      'attrs': self.dumps(
                                                                                          dict(domain.attrib))
                                                                                  })

    def _build_icd(self, project):
        if {'name', 'version', 'id'} <= set(project.attrib.keys()) and project.tag == 'Project':
            project_object, flag = models.IcdProject.objects.update_or_create(project_id=project.get('id'),
                                                                              defaults={
                                                                                  'name': project.get('name'),
                                                                                  'version': project.get('version'),
                                                                                  'attrs': self.dumps(
                                                                                      dict(project.attrib))
                                                                              })
            products = project.xpath(BaseTool.xpath_expression_generator('Products', self._product_attrs))
            for product in products:
                product_object, _ = models.IcdProduct.objects.update_or_create(product_id=product.get('id'),
                                                                               defaults={
                                                                                   'name': product.get('name'),
                                                                                   'version': product.get('version'),
                                                                                   'icd_project': project_object,
                                                                                   'attrs': self.dumps(
                                                                                       dict(product.attrib))
                                                                               })
                buses = product.xpath(BaseTool.xpath_expression_generator('Bus', self._bus_attrs))
                for bus in buses:
                    self._parse(bus, product_object)
            if not flag:
                message_framework.warning(self.request, '数据库中存在同名项目，已覆盖')
        else:
            raise AssertionError('根节点不是Project或属性不全')

    def _validate(self, project):
        if {'name', 'version', 'id'} <= set(project.attrib.keys()) and project.tag == 'Project':
            products = project.xpath(BaseTool.xpath_expression_generator('Products', self._product_attrs))
            for product in products:
                buses = product.xpath(BaseTool.xpath_expression_generator('Bus', self._bus_attrs))
                for bus in buses:
                    bus_type = bus.get('type')
                    message_attrs = self.message_attrs_dict.get(bus_type, [])
                    messages = bus.xpath(BaseTool.xpath_expression_generator('Message', message_attrs))
                    for message in messages:
                        signals = message.xpath(BaseTool.xpath_expression_generator('Signal', self._signal_attrs))
                        for signal in signals:
                            domains = signal.xpath(BaseTool.xpath_expression_generator('Domain', self._domain_attrs))
                            for domain in domains:
                                pass
        else:
            raise BaseException('根节点不是Project或属性不全')

    def form_valid(self, form):
        # TODO 针对不同的生成工具，设计一套通用灵活的解析方案，目前只有ICDSys，因此暂时不需要动手。
        try:
            icd_type = form.cleaned_data['icd_type']
            project = etree.XML(form.cleaned_data['file'].read())
            self._validate(project)
            self._build_icd(project)
        except XMLSyntaxError as e:
            message_framework.error(self.request, 'XML解析失败,{reason}'.format(reason=e))
            return super(UploadIcdFormView, self).form_invalid(form)
        except BaseException as e:
            message_framework.error(self.request, e)
            return super(UploadIcdFormView, self).form_invalid(form)
        return super(UploadIcdFormView, self).form_valid(form)


class IcdProjectListView(ListView):
    model = models.IcdProject
    template_name = 'ate_tasks/icd/icd_project_list.html'
    paginate_by = 15


class IcdProjectDeleteView(DeleteView):
    model = models.IcdProject
    success_url = reverse_lazy('ate_tasks:icd-project-list')
    template_name = 'ate_tasks/icd/icd_project_confirm_delete.html'


class IcdProjectDetailView(DetailView):
    model = models.IcdProject
    template_name = 'ate_tasks/icd/icd_project_detail.html'

    def get_context_data(self, **kwargs):
        icd_project = self.object
        context = super(IcdProjectDetailView, self).get_context_data(**kwargs)
        context['icd_project_tree'] = json.dumps([icd_project.tree_node], ensure_ascii=False)
        return context


class QueryIcdNodeAttrsView(View):
    model_type_dict = {
        'domain': models.IcdDomain,
        'signal': models.IcdSignal,
        'message': models.IcdMessage,
        'product': models.IcdProduct,
        'project': models.IcdProject
    }

    def get(self, request):
        pk = int(request.GET.get('id'))
        model_type = request.GET.get('type')
        current_model = self.model_type_dict.get(model_type)
        current_object = current_model.objects.get(pk=pk)
        attrs = json.loads(current_object.attrs, encoding='utf-8')
        table_attrs = 'border="1" class="table table-condensed table-bordered table-hover"'
        response = json2html.convert(json=attrs, table_attributes=table_attrs)
        return HttpResponse(response)
