# coding=utf-8
from django import forms
from django.forms import ModelForm, Textarea
from django.forms.models import inlineformset_factory

import ate_tasks.models as models


class ValidationPhaseForm(ModelForm):
    class Meta:
        model = models.ValidationPhase
        fields = "__all__"
        widgets = {
            'description': Textarea(attrs={'style': 'width:100%'}),
        }


class ProductForm(ModelForm):
    class Meta:
        model = models.Product
        fields = "__all__"
        widgets = {
            'description': Textarea(attrs={'style': 'width:100%'}),
        }


class ProductInstanceForm(ModelForm):
    class Meta:
        model = models.ProductInstance
        fields = "__all__"
        widgets = {
            'description': Textarea(attrs={'style': 'width:100%'}),
        }


class ProjectForm(ModelForm):
    class Meta:
        model = models.Project
        fields = "__all__"
        widgets = {
            'description': Textarea(attrs={'style': 'width:100%'}),
        }


class TestItemForm(ModelForm):
    class Meta:
        model = models.TestItem
        fields = "__all__"
        widgets = {
            'description': Textarea(attrs={'style': 'width:100%'}),
            'code': Textarea(attrs={'style': 'width:100%'}),
            'parameters': Textarea(attrs={'style': 'width:100%'}),
        }


class TaskInstanceForm(ModelForm):
    class Meta:
        model = models.TaskInstance
        fields = ['task', 'product_instance', 'creator']


class TaskForm(ModelForm):
    class Meta:
        model = models.Task
        fields = "__all__"
        widgets = {
            'description': Textarea(attrs={'style': 'width:100%'}),
        }


TaskStepFormSet = inlineformset_factory(models.Task, models.TaskStep, fields=['order', 'test_item'], can_delete=True,
                                        extra=1)


class KeywordForm(ModelForm):
    class Meta:
        model = models.KeyWord
        fields = "__all__"
        widgets = {
            'description': Textarea(attrs={'style': 'width:100%'}),
            'example_code': Textarea(attrs={'style': 'width:100%'}),
        }


class TestItemFilterForm(forms.Form):
    project = forms.ChoiceField(label='项目')
    product = forms.ChoiceField(label='产品')
    creator = forms.ChoiceField(label='创建者')

    def __init__(self, *args, **kwargs):
        super(TestItemFilterForm, self).__init__(*args, **kwargs)
        project_choices = [(-1, '全部')] + [(project.id, project.name) for project in
                                          models.Project.objects.all()]
        product_choices = [(-1, '全部')] + [(product.id, product.name) for product in
                                          models.Product.objects.all()]
        creator_choices = [(-1, '全部')] + [(creator, creator) for creator in
                                          set([item[0] for item in
                                               models.TestItem.objects.all().values_list('creator', flat=False)])]
        self.fields['project'].choices = project_choices
        self.fields['product'].choices = product_choices
        self.fields['creator'].choices = creator_choices
