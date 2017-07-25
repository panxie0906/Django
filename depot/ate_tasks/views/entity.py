# coding=utf-8
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView

import ate_tasks.forms as forms
import ate_tasks.models as models

from .base import BaseEntityViewGenerator, BaseUpdateView


class TestItemViewGenerator(BaseEntityViewGenerator):
    success_url = reverse_lazy('ate_tasks:entity-test-item-list')
    model = models.TestItem
    paginate_by = 15
    entity_name = 'test_item'
    form_class = forms.TestItemForm

    @classmethod
    def get_list_view(cls):
        class Index(ListView):
            template_formatter = 'ate_tasks/entity/{name}_list.html'
            model = cls.model
            template_name = template_formatter.format(name=cls.entity_name)
            paginate_by = cls.paginate_by

            def get_queryset(self):
                fields = ['project', 'product']
                item_filter = {field + '_id': self.request.GET[field] for field in fields if
                               self.request.GET.get(field, '-1') != '-1'}
                creator = self.request.GET.get('creator', '-1')
                if creator != '-1':
                    item_filter['creator'] = creator
                new_context = models.TestItem.objects.all().filter(**item_filter)
                return new_context

            def get_context_data(self, **kwargs):
                context = super(Index, self).get_context_data(**kwargs)
                context['project'] = self.request.GET.get('project', '-1')
                context['product'] = self.request.GET.get('product', '-1')
                context['creator'] = self.request.GET.get('creator', '-1')
                initial = {'project': context['project'], 'product': context['product'], 'creator': context['creator']}
                filter_form = forms.TestItemFilterForm(initial=initial)
                context['filter_form'] = filter_form
                context['query_params'] = initial
                return context

        return Index


class TaskViewGenerator(BaseEntityViewGenerator):
    success_url = reverse_lazy('ate_tasks:entity-task-list')
    model = models.Task
    paginate_by = 15
    entity_name = 'task'
    form_class = forms.TaskForm

    @classmethod
    def get_update_view(cls):
        class Update(BaseUpdateView):
            template_formatter = 'ate_tasks/entity/{name}_update_form.html'
            model = cls.model
            template_name = template_formatter.format(name=cls.entity_name)
            form_class = cls.form_class

            def get(self, request, *args, **kwargs):
                self.object = self.model.objects.get(pk=int(kwargs['pk']))
                form = forms.TaskForm(instance=self.object)
                task_step_form = forms.TaskStepFormSet(instance=self.object)
                for step_form in task_step_form.forms:
                    step_form.fields['test_item'].queryset = models.TestItem.objects.filter(project=self.object.project,
                                                                                            product=self.object.product)
                return self.render_to_response(
                    self.get_context_data(form=form, task_step_form=task_step_form))

            def post(self, request, *args, **kwargs):
                self.object = self.model.objects.get(pk=int(kwargs['pk']))
                form = forms.TaskForm(self.request.POST, instance=self.object)
                task_step_form = forms.TaskStepFormSet(self.request.POST, instance=self.object)

                if form.is_valid() and task_step_form.is_valid():
                    return self.form_valid(form, task_step_form=task_step_form)
                else:
                    return self.form_invalid(form, task_step_form=task_step_form)

            def form_valid(self, form, task_step_form=None):
                self.object = form.save()
                task_step_form.instance = self.object
                task_step_form.save()
                return HttpResponseRedirect(self.get_success_url())

            def form_invalid(self, form, task_step_form=None):

                return self.render_to_response(
                    self.get_context_data(form=form,
                                          task_step_form=task_step_form))

        return Update


def generator_factory(success_pattern, model, paginate_by, entity_name, form_class):
    generator = type('{name}_view_generator'.format(name=entity_name), (BaseEntityViewGenerator,), {
        'success_url': reverse_lazy(success_pattern),
        'model': model,
        'paginate_by': paginate_by,
        'entity_name': entity_name,
        'form_class': form_class
    })

    return generator


ValidationPhaseViewGenerator = generator_factory('ate_tasks:entity-validation-phase-list', models.ValidationPhase, 15,
                                                 'validation_phase', forms.ValidationPhaseForm)

ProjectViewGenerator = generator_factory('ate_tasks:entity-project-list', models.Project, 15, 'project',
                                         forms.ProjectForm)
ProductViewGenerator = generator_factory('ate_tasks:entity-product-list', models.Product, 15, 'product',
                                         forms.ProductForm)
ProductInstanceViewGenerator = generator_factory('ate_tasks:entity-product-instance-list', models.ProductInstance, 15,
                                                 'product_instance', forms.ProductInstanceForm)
KeywordViewGenerator = generator_factory('ate_tasks:entity-keyword-list', models.KeyWord, 15, 'keyword',
                                         forms.KeywordForm)

TaskInstanceViewGenerator = generator_factory('ate_tasks:entity-task-instance-list', models.TaskInstance, 15,
                                              'task_instance', forms.TaskInstanceForm)
