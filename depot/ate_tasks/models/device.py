# coding=utf-8
import json
from collections import OrderedDict

from django.db import models
from django.urls import reverse
from jinja2 import Template

from .base import BaseTool
from .icd import IcdMessage


class ServiceNode(models.Model):
    ip = models.GenericIPAddressField(verbose_name='ip', default='127.0.0.1')

    @property
    def tree_node(self):
        node = BaseTool.create_node(True, self.ip, 'service_node', node_id=self.id, tags=[self.devices.count()])

        bus_list = set([item[0] for item in self.devices.all().values_list('bus', flat=False)])
        for bus in bus_list:
            bus_node = BaseTool.create_node(True, bus, 'bus', node_id=bus)
            for device in self.devices.all().filter(bus=bus):
                bus_node['children'].append(device.tree_node)
            node['children'].append(bus_node)
        return node

    def __str__(self):
        return self.ip

    class Meta:
        ordering = ('ip',)
        verbose_name = '服务节点'
        verbose_name_plural = '服务节点列表'


class Device(models.Model):
    name = models.CharField(max_length=255, verbose_name='name')
    device_id = models.CharField(max_length=255, verbose_name='id', unique=True)
    device_info = models.TextField(blank=True, verbose_name='设备信息')
    bus = models.CharField(max_length=255, verbose_name='总线类型')
    service_node = models.ForeignKey(ServiceNode, on_delete=models.CASCADE, related_name='devices', verbose_name='所属节点')
    description = models.TextField(blank=True, verbose_name='描述信息')
    parameters = models.TextField(blank=True, verbose_name='配置参数', default=[])
    channels = models.TextField(blank=True, verbose_name='通道信息', default=[])
    bindings = models.TextField(blank=True, verbose_name='消息绑定')
    is_running = models.BooleanField(default=False, verbose_name='运行中')

    @property
    def tree_node(self):
        node = BaseTool.create_node(False, self.__str__(), 'service_node',
                                    node_id=self.id,
                                    href=reverse('ate_tasks:device-message-binding', kwargs={'pk': self.id}))
        return node

    def __str__(self):
        return '{name}({id})'.format(name=self.name, id=self.device_id)

    class Meta:
        ordering = ('name',)
        verbose_name = '测试资源'
        verbose_name_plural = '测试资源列表'


# TODO 增加不同总线类型的配置信息
class BusType(models.Model):
    name = models.CharField(max_length=255)
    device_binding_schema = models.TextField(blank=True, help_text='schema需要经过处理才能传递')
    device_binding_option = models.TextField(blank=True, help_text='option一般原封不动传递')
    icd_message_schema = models.TextField(blank=True, help_text='消息内容编辑时需要用到', default='{}')
    icd_message_option = models.TextField(blank=True, help_text='消息内容编辑时需要用到', default='{}')

    def __str__(self):
        return self.name

    @property
    def binding_schema(self):
        template = Template(self.device_binding_schema)
        choices = [message.name for message in IcdMessage.objects.all().filter(bus=self.name)]
        result = template.render(messages=json.dumps(choices, ensure_ascii=False))
        schema = json.loads(result, encoding='utf-8', object_pairs_hook=OrderedDict)
        return schema

    @property
    def binding_option(self):
        option = json.loads(self.device_binding_option, encoding='utf-8', object_pairs_hook=OrderedDict)
        return option

    @property
    def message_schema(self):
        schema = json.loads(self.icd_message_schema, encoding='utf-8', object_pairs_hook=OrderedDict)
        return schema

    @property
    def message_option(self):
        option = json.loads(self.icd_message_option, encoding='utf-8', object_pairs_hook=OrderedDict)
        return option

    class Meta:
        ordering = ('name',)
        verbose_name = '总线类型'
        verbose_name_plural = '总线类型列表'
