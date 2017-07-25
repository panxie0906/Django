# coding=utf-8

import json

from django.db import models

from .base import BaseTool, IcdBaseModel


class IcdProject(IcdBaseModel):
    name = models.CharField(max_length=255)
    version = models.CharField(max_length=255)
    project_id = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

    @property
    def tree_node(self):
        node = BaseTool.create_node(True, self.name, 'project', tags=[self.products.count()], node_id=self.id)
        for product in self.products.all():
            node['children'].append(product.tree_node)
        return node

    @property
    def simple_node(self):
        node = BaseTool.create_node(True, self.name, 'project', node_id=self.id)
        for product in self.products.all():
            node['children'].append(product.simple_node)
        return node

    @property
    def xml_dict(self):
        attrs = json.loads(self.attrs, encoding='utf-8')
        xml_attrs = {'@{name}'.format(name=key): value for key, value in attrs.items()}

        products = [product.xml_dict for product in self.products.all()]
        xml_attrs['Products'] = products
        xml_attrs = {'Project': xml_attrs}
        return xml_attrs


class IcdProduct(IcdBaseModel):
    name = models.CharField(max_length=255)
    version = models.CharField(max_length=255)
    product_id = models.CharField(max_length=255, unique=True)
    icd_project = models.ForeignKey(IcdProject, on_delete=models.CASCADE, related_name='products')

    @property
    def simple_node(self):
        node = BaseTool.create_node(True, self.name, 'product', node_id=self.id)
        bus_list = set([item[0] for item in self.messages.all().values_list('bus', flat=False)])
        for bus in bus_list:
            bus_node = BaseTool.create_node(True, bus, 'bus', node_id=bus, selectable=False)
            for message in self.messages.all().filter(bus=bus):
                bus_node['children'].append(message.simple_node)
            node['children'].append(bus_node)
        return node

    @property
    def tree_node(self):
        node = BaseTool.create_node(True, self.name, 'product', tags=[self.messages.count()], node_id=self.id)
        bus_list = set([item[0] for item in self.messages.all().values_list('bus', flat=False)])
        for bus in bus_list:
            bus_node = BaseTool.create_node(True, bus, 'bus', node_id=bus, selectable=False)
            for message in self.messages.all().filter(bus=bus):
                bus_node['children'].append(message.tree_node)
            node['children'].append(bus_node)
        return node

    @property
    def xml_dict(self):
        attrs = json.loads(self.attrs, encoding='utf-8')
        xml_attrs = {'@{name}'.format(name=key): value for key, value in attrs.items()}

        bus_list = set([item[0] for item in self.messages.all().values_list('bus', flat=False)])
        buses = []
        for bus in bus_list:
            bus_messages = [message.xml_dict for message in self.messages.all().filter(bus=bus)]
            bus_xml_dict = {'@type': bus, 'Message': bus_messages}
            buses.append(bus_xml_dict)
        xml_attrs['Bus'] = buses
        return xml_attrs


class IcdMessage(IcdBaseModel):
    name = models.CharField(max_length=255)
    message_id = models.CharField(max_length=255, unique=True)
    bus = models.CharField(max_length=255)
    icd_product = models.ForeignKey(IcdProduct, on_delete=models.CASCADE, related_name='messages')

    @property
    def simple_node(self):
        node = BaseTool.create_node(False, self.name, 'message', node_id=self.id, expanded=False)
        return node

    @property
    def tree_node(self):
        node = BaseTool.create_node(True, self.name, 'message', tags=[self.signals.count()], node_id=self.id,
                                    expanded=False)
        for signal in self.signals.all():
            node['children'].append(signal.tree_node)
        return node

    @property
    def xml_dict(self):
        attrs = json.loads(self.attrs, encoding='utf-8')
        xml_attrs = {'@{name}'.format(name=key): value for key, value in attrs.items()}
        signals = [signal.xml_dict for signal in self.signals.all()]
        xml_attrs['Signal'] = signals
        return xml_attrs

    @property
    def icd_init_data(self):
        init_data = {
            'name': self.name,
            'id': self.message_id,
            'bus_type': self.bus,
            'product': self.icd_product.name
        }
        signals = []
        for signal in self.signals.all():
            domains = [{'name': domain.name, 'type': domain.domain_type, 'startbits': domain.start_bits,
                        'endbits': domain.end_bits, 'remark': domain.remark, 'value': ''} for domain in
                       signal.domains.all()]
            signals.append({'name': signal.name, 'length': signal.length, 'start': signal.start, 'end': signal.end,
                            'domains': domains})
        init_data['signals'] = signals
        return init_data


class IcdSignal(IcdBaseModel):
    name = models.CharField(max_length=255)
    length = models.IntegerField()
    start = models.IntegerField()
    end = models.IntegerField()
    message = models.ForeignKey(IcdMessage, on_delete=models.CASCADE, related_name='signals')

    @property
    def tree_node(self):
        node = BaseTool.create_node(True, self.name, 'signal', tags=[self.domains.count()], node_id=self.id,
                                    expanded=False)
        for domain in self.domains.all():
            node['children'].append(domain.tree_node)
        return node

    @property
    def xml_dict(self):
        attrs = json.loads(self.attrs, encoding='utf-8')
        xml_attrs = {'@{name}'.format(name=key): value for key, value in attrs.items()}
        domains = [domain.xml_dict for domain in self.domains.all()]
        xml_attrs['Domain'] = domains
        return xml_attrs


class IcdDomain(IcdBaseModel):
    name = models.CharField(max_length=255)
    domain_type = models.CharField(max_length=255)
    start_bits = models.IntegerField()
    end_bits = models.IntegerField()
    remark = models.TextField(blank=True)
    signal = models.ForeignKey(IcdSignal, on_delete=models.CASCADE, related_name='domains')

    @property
    def tree_node(self):
        node = BaseTool.create_node(False, self.name, 'domain', node_id=self.id, expanded=False)
        return node

    @property
    def xml_dict(self):
        attrs = json.loads(self.attrs, encoding='utf-8')
        xml_attrs = {'@{name}'.format(name=key): value for key, value in attrs.items()}
        return xml_attrs
