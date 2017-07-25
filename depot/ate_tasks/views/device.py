import json
from collections import OrderedDict

from django.contrib import messages as message_framework
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import FormView, ListView, UpdateView
from lxml import etree
from lxml.etree import XMLSyntaxError

import ate_tasks.models as models
from ate_tasks.forms import DeviceUploadForm
from .base import BaseTool


class DeviceListView(ListView):
    model = models.ServiceNode
    template_name = 'ate_tasks/device/navigator.html'

    @BaseTool.context_add_device_tree
    def get_context_data(self, **kwargs):
        context = super(DeviceListView, self).get_context_data(**kwargs)
        return context


class DeviceMessageBindingView(UpdateView):
    model = models.Device
    fields = '__all__'
    template_name = 'ate_tasks/device/message_binding.html'

    def post(self, request, *args, **kwargs):
        bindings = request.POST['bindings']
        self.object = self.get_object()
        device = get_object_or_404(models.Device, pk=self.object.pk)
        device.bindings = bindings
        device.save()
        return super(DeviceMessageBindingView, self).post(request, *args, **kwargs)

    @BaseTool.context_add_device_tree
    @BaseTool.context_add_simple_icd_tree
    def get_context_data(self, **kwargs):
        context = super(DeviceMessageBindingView, self).get_context_data(**kwargs)
        return context


class DeviceUploadView(FormView):
    template_name = 'ate_tasks/device/upload_file.html'
    form_class = DeviceUploadForm
    success_url = reverse_lazy('ate_tasks:device-list')

    def __init__(self):
        super(DeviceUploadView, self).__init__()
        self._channel_list_handler = {
            'RS422': self._channel_list_default_handler,
            '1553B': self._channel_list_1553b_handler,
            'Switches': self._channel_list_default_handler,
            'Analog': self._channel_list_default_handler,
            'Test': self._channel_list_default_handler
        }
        self._device_attrs_dict = {
            'RS422': ['name', 'id', 'channelsum'],
            '1553B': ['name', 'mode', 'id', 'num'],
            'Switches': ['name', 'id', 'mode', 'num'],
            'Analog': ['name', 'id', 'num'],
            'Test': ['name', 'id', 'num'],
        }
        self._parameter_attrs = ['name', 'range']
        self._channel_attrs_dict = {
            'RS422': ['name', 'com', 'remark'],
            '1553B': ['name', 'type', 'id', 'remark'],
            'Switches': [],
            'Analog': ['name', 'id', 'minVal', 'maxVal', 'remark'],
            'Test': ['name', 'remark'],
        }

    @staticmethod
    def _channel_list_default_handler(channels):
        return [dict(channel.attrib) for channel in channels]

    @classmethod
    def _channel_list_1553b_handler(cls, channels):
        channel_list = []
        for channel in channels:
            attrs_dict = {}
            bus_ab_attrs = ['id']
            bus_a = channel.xpath(BaseTool.xpath_expression_generator('BUS_A', bus_ab_attrs))[0]
            bus_b = channel.xpath(BaseTool.xpath_expression_generator('BUS_B', bus_ab_attrs))[0]
            attrs_dict['BUS_A'] = {'id': bus_a.get('id')}
            attrs_dict['BUS_B'] = {'id': bus_b.get('id')}
            attrs_dict.update(dict(channel.attrib))
            channel_list.append(attrs_dict)
        return channel_list

    def _parse(self, bus, service_node_object, channels_handler):
        bus_type = bus.get('type')
        device_attrs = self._device_attrs_dict[bus_type]
        devices = bus.xpath(BaseTool.xpath_expression_generator('Device', device_attrs))
        for device in devices:
            description = device.xpath(BaseTool.xpath_expression_generator('Description', []))
            description = '' if not description else description[0].text

            parameters = device.xpath(BaseTool.xpath_expression_generator('Parameters', self._parameter_attrs))
            parameters_list = [dict(parameter.attrib) for parameter in parameters]

            channels = device.xpath(BaseTool.xpath_expression_generator('Channel', self._channel_attrs_dict[bus_type]))
            channels_list = channels_handler(channels)
            device_object, _ = models.Device.objects.update_or_create(device_id=device.get('id'),
                                                                      defaults={
                                                                          'name': device.get('name'),
                                                                          'bus': bus_type,
                                                                          'service_node': service_node_object,
                                                                          'description': description,
                                                                          'parameters': json.dumps(
                                                                              parameters_list,
                                                                              ensure_ascii=False, indent=4),
                                                                          'channels': json.dumps(
                                                                              channels_list,
                                                                              ensure_ascii=False, indent=4),
                                                                          'device_info': json.dumps(
                                                                              dict(device.attrib),
                                                                              ensure_ascii=False, indent=4)
                                                                      })
            device_info = {'@{key}'.format(key=key): value for key, value in (
                json.loads(device_object.device_info, encoding='utf-8', object_pairs_hook=OrderedDict)).items()}
            device_info['@bus_type'] = device_object.bus
            device_info['@description'] = description
            channels = json.loads(device_object.channels, encoding='utf-8', object_pairs_hook=OrderedDict)
            bindings = {'device': device_info, 'channels': channels} if channels else {'device': device_info}
            device_object.bindings = json.dumps(bindings, ensure_ascii=False, indent=4)
            device_object.save()

    def _build_service_node(self, service_node):
        if {'ip'} <= set(service_node.attrib.keys()) and service_node.tag == 'ServiceNode':
            service_node_object, flag = models.ServiceNode.objects.update_or_create(ip=service_node.get('ip'))
            bus_attrs = ['type']
            buses = service_node.xpath(BaseTool.xpath_expression_generator('Bus', bus_attrs))
            for bus in buses:
                bus_type = bus.get('type')
                channel_list_handler = self._channel_list_handler[bus_type]
                self._parse(bus, service_node_object, channel_list_handler)
            if not flag:
                message_framework.warning(self.request, '数据库中存在同名项目，已覆盖')
        else:
            raise AssertionError('根节点不是ServiceNode或属性不全')

    def form_valid(self, form):
        try:
            service_node = etree.XML(form.cleaned_data['file'].read())
            self._build_service_node(service_node)
        except XMLSyntaxError as e:
            message_framework.error(self.request, 'XML解析失败,{reason}'.format(reason=e))
            return super(DeviceUploadView, self).form_invalid(form)
        except BaseException as e:
            message_framework.error(self.request, e)
            return super(DeviceUploadView, self).form_invalid(form)
        return super(DeviceUploadView, self).form_valid(form)

    @BaseTool.context_add_device_tree
    def get_context_data(self, **kwargs):
        context = super(DeviceUploadView, self).get_context_data(**kwargs)
        return context
