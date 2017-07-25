# coding=utf-8
import json

from django.views.generic import CreateView, DeleteView, ListView, UpdateView

import depotapp.models as models


class BaseCreateView(CreateView):
    def __init__(self, **kwargs):
        super(BaseCreateView, self).__init__(**kwargs)
        self.object = None

    def get_context_data(self, **kwargs):
        verbose_name = self.model._meta.verbose_name.title()
        title = '新建 {verbose_name}'.format(verbose_name=verbose_name)
        return super(BaseCreateView, self).get_context_data(title=title, verbose_name=verbose_name, **kwargs)


class BaseDeleteView(DeleteView):
    def get_context_data(self, **kwargs):
        verbose_name = self.model._meta.verbose_name.title()
        title = '删除 {verbose_name}'.format(verbose_name=verbose_name)
        return super(BaseDeleteView, self).get_context_data(title=title, verbose_name=verbose_name, **kwargs)


class BaseUpdateView(UpdateView):
    def __init__(self, **kwargs):
        super(BaseUpdateView, self).__init__(**kwargs)
        self.object = None

    def get_context_data(self, **kwargs):
        verbose_name = self.model._meta.verbose_name.title()
        title = '编辑 {verbose_name}'.format(verbose_name=verbose_name)
        return super(BaseUpdateView, self).get_context_data(title=title, verbose_name=verbose_name, **kwargs)


class BaseEntityViewGenerator:
    success_url = None
    model = None
    paginate_by = None
    entity_name = None
    form_class = None

    @classmethod
    def get_list_view(cls):
        class Index(ListView):
            template_formatter = 'ate_tasks/entity/{name}_list.html'
            model = cls.model
            template_name = template_formatter.format(name=cls.entity_name)
            paginate_by = cls.paginate_by

        return Index

    @classmethod
    def get_create_view(cls):
        class Create(BaseCreateView):
            template_formatter = 'ate_tasks/entity/{name}_create_form.html'
            model = cls.model
            template_name = template_formatter.format(name=cls.entity_name)
            form_class = cls.form_class
            success_url = cls.success_url

        return Create

    @classmethod
    def get_update_view(cls):
        class Update(BaseUpdateView):
            template_formatter = 'ate_tasks/entity/{name}_update_form.html'
            model = cls.model
            template_name = template_formatter.format(name=cls.entity_name)
            form_class = cls.form_class
            success_url = cls.success_url

        return Update

    @classmethod
    def get_delete_view(cls):
        class Delete(BaseDeleteView):
            template_formatter = 'ate_tasks/entity/{name}_confirm_delete.html'
            model = cls.model
            template_name = template_formatter.format(name=cls.entity_name)
            success_url = cls.success_url

        return Delete


class BaseTool:
    @staticmethod
    def add_rules_to_simple_icd_tree(fun):
        def recursion(obj, rules):
            if type(obj) is list:
                for item in obj:
                    recursion(item, rules)
            elif type(obj) is dict:
                node_type = obj.get('type')
                if node_type == 'message':
                    if int(obj.get('id')) in rules:
                        obj['selected'] = True
                for key, value in obj.items():
                    recursion(value, rules)
            else:
                pass

        def inner(*args, **kwargs):
            context = fun(*args, **kwargs)
            if context['object'].rules != '':
                rules = list(map(int, context['object'].rules.split('-')))
                tree = json.loads(context.get('simple_icd_tree', []))
                recursion(tree, rules)
                context['simple_icd_tree'] = json.dumps(tree, ensure_ascii=False)
            return context

        return inner

    @staticmethod
    def get_device_fancy_tree(dumps=False):
        tree_nodes = []
        for service_node in models.ServiceNode.objects.all():
            tree_nodes.append(service_node.tree_node)
        if dumps:
            return json.dumps(tree_nodes, ensure_ascii=False, indent=4)
        else:
            return tree_nodes

    @classmethod
    def context_add_device_fancy_tree(cls, fun):
        def inner(*args, **kwargs):
            context = fun(*args, **kwargs)
            context['device_tree'] = cls.get_device_tree(dumps=True)
            return context

        return inner

    @classmethod
    def context_add_device_tree(cls, fun):
        def inner(*args, **kwargs):
            context = fun(*args, **kwargs)
            context['device_tree'] = cls.get_device_tree(dumps=True)
            return context

        return inner

    @classmethod
    def context_add_simple_icd_tree(cls, fun):
        def inner(*args, **kwargs):
            context = fun(*args, **kwargs)
            context['simple_icd_tree'] = cls.get_simple_icd_tree(dumps=True)
            return context

        return inner

    @classmethod
    def context_add_icd_tree(cls, fun):
        def inner(*args, **kwargs):
            context = fun(*args, **kwargs)
            context['icd_tree'] = cls.get_icd_tree(dumps=True)
            return context

        return inner

    @staticmethod
    def get_simple_icd_tree(dumps=False):
        icd_tree = []
        for project in models.IcdProject.objects.all():
            icd_tree.append(project.simple_node)
        if dumps:
            return json.dumps(icd_tree, ensure_ascii=False, indent=4)
        else:
            return icd_tree

    @staticmethod
    def get_icd_tree(dumps=False):
        icd_tree = []
        for project in models.IcdProject.objects.all():
            icd_tree.append(project.tree_node)
        if dumps:
            return json.dumps(icd_tree, ensure_ascii=False, indent=4)
        else:
            return icd_tree

    @staticmethod
    def get_icd_project_tree(pk, dumps=False):
        project = models.IcdProject.objects.get(pk=pk)
        icd_tree = [project.tree_node]
        if dumps:
            return json.dumps(icd_tree, ensure_ascii=False, indent=4)
        else:
            return icd_tree

    @staticmethod
    def get_device_tree(dumps=False):
        tree_nodes = []
        for service_node in models.ServiceNode.objects.all():
            tree_nodes.append(service_node.tree_node)
        if dumps:
            return json.dumps(tree_nodes, ensure_ascii=False, indent=4)
        else:
            return tree_nodes

    @staticmethod
    def xpath_expression_generator(element_name, attrs):
        if attrs:
            expression = './{element_name}[{attrs}]'.format(element_name=element_name,
                                                            attrs=' and '.join(
                                                                ['@{attr}'.format(attr=attr) for attr in attrs]))
        else:
            expression = './{element_name}'.format(element_name=element_name)
        return expression
