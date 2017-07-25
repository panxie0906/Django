# coding=utf-8

import json
from collections import OrderedDict
from random import choice

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.generic import View

import ate_tasks.models as models
from .base import BaseTool


class GetTreeView(View):
    tree_handlers = {
        'device_tree': BaseTool.get_device_tree,
        'simple_icd_tree': BaseTool.get_simple_icd_tree,
        'icd_tree': BaseTool.get_icd_tree
    }

    def get(self, request):
        tree = []
        tree_type = request.GET.get('type')
        if tree_type:
            handler = self.tree_handlers.get(tree_type)
            if handler:
                tree = handler(dumps=False)
        return JsonResponse(tree, json_dumps_params={'ensure_ascii': False, 'indent': 4}, safe=False)


class GetBusTypeBindingSchema(View):
    @staticmethod
    def get(request):
        bus = request.GET.get('bus_type')
        bus_type = get_object_or_404(models.BusType, name=bus)
        return JsonResponse(bus_type.binding_schema, json_dumps_params={'ensure_ascii': False, 'indent': 4}, safe=False)


class GetBusTypeBindingOption(View):
    @staticmethod
    def get(request):
        bus = request.GET.get('bus_type')
        bus_type = get_object_or_404(models.BusType, name=bus)
        return JsonResponse(bus_type.binding_option, json_dumps_params={'ensure_ascii': False, 'indent': 4}, safe=False)


class GetBusTypeMessageSchema(View):
    @staticmethod
    def get(request):
        bus = request.GET.get('bus_type')
        bus_type = get_object_or_404(models.BusType, name=bus)
        return JsonResponse(bus_type.message_schema, json_dumps_params={'ensure_ascii': False, 'indent': 4}, safe=False)


class GetBusTypeMessageOption(View):
    @staticmethod
    def get(request):
        bus = request.GET.get('bus_type')
        bus_type = get_object_or_404(models.BusType, name=bus)
        return JsonResponse(bus_type.message_option, json_dumps_params={'ensure_ascii': False, 'indent': 4}, safe=False)


class GetDeviceBinding(View):
    @staticmethod
    def get(request):
        pk = request.GET.get('pk')
        device = get_object_or_404(models.Device, pk=pk)
        bindings = json.loads(device.bindings, encoding='utf-8', object_pairs_hook=OrderedDict)
        return JsonResponse(bindings, json_dumps_params={'ensure_ascii': False, 'indent': 4}, safe=False)


class GetRandomMessageInitData(View):
    @staticmethod
    def get(request):
        message = choice(list(models.IcdMessage.objects.all().filter(bus='Test')))
        return JsonResponse(message.icd_init_data, json_dumps_params={'ensure_ascii': False, 'indent': 4}, safe=False)
