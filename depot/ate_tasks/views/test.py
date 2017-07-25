import json
from io import StringIO

import xmltodict
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render

import ate_tasks.models as models
from .base import BaseTool


def form_test(request, pk):
    if request.method == 'POST':
        bindings = request.POST['bindings']
        device = get_object_or_404(models.Device, pk=pk)
        device.bindings = bindings
        device.save()
    else:
        pass
    return render(request, 'ate_tasks/test/form_test.html')


def fancy_tree_test(request):
    tree = BaseTool.get_simple_icd_tree()

    return JsonResponse(tree, json_dumps_params={'ensure_ascii': False, 'indent': 4}, safe=False)


def config_test(request):
    projects = models.IcdProject.objects.all()
    my_io = StringIO()
    for project in projects:
        root = {
            'Project': {
                '@name': project.name,
                '@version': project.version,
                '@id': project.project_id,
                '@ICDversion': '1.00',
                'Products': []
            }
        }
        for product in project.products.all():
            product_element = {
                '@name': product.name,
                '@version': product.version,
                '@id': product.product_id,
                '@ICDversion': '1.00',
                "Device": []
            }
            for device in models.Device.objects.all():
                product_element['Device'].append(json.loads(device.bindings, encoding='utf-8'))
            root['Project']['Products'].append(product_element)
            my_io.write(xmltodict.unparse(root) + '\n')
    return render(request, 'ate_tasks/test/config_test.html', {'data': my_io.getvalue()})
