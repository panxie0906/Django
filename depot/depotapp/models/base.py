# coding=utf-8
import abc

import xmltodict
from django.db import models


class BaseModel(models.Model):
    name = models.CharField(max_length=255, verbose_name='名称', unique=True)
    creator = models.CharField(max_length=255, verbose_name='创建者')
    created = models.DateTimeField(verbose_name='创建日期', auto_now_add=True)
    modified = models.DateTimeField(verbose_name='修改日期', auto_now=True)
    description = models.TextField(verbose_name='描述信息', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class IcdBaseModel(models.Model):
    attrs = models.TextField(blank=True, default='{}')

    @abc.abstractproperty
    def xml_dict(self):
        """返回可以被反序列化为xml的字典(可以被xmltodict库识别)"""

    @property
    def xml(self):
        return xmltodict.unparse(self.xml_dict)

    class Meta:
        abstract = True


class BaseTool:
    node_icon = {
        'service_node': 'glyphicon glyphicon-home',
        'bus': 'glyphicon glyphicon-sort',
        'device': 'glyphicon glyphicon-star',
        'project': 'glyphicon glyphicon-home',
        'product': 'glyphicon glyphicon-road',
        'message': 'glyphicon glyphicon-inbox',
        'signal': 'glyphicon glyphicon-bookmark',
        'domain': 'glyphicon glyphicon-star'
    }

    @classmethod
    def create_node(cls, has_child, text, node_type, tags=None, node_id=None, **kwargs):
        icon = cls.node_icon.get(node_type)
        node = {
            'icon': icon,
            'title': text,
            'type': node_type
        }
        if has_child:
            node['children'] = []
            node['expanded'] = True

        if node_id:
            node['id'] = node_id
        node.update(**kwargs)
        return node
