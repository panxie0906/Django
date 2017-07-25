# coding=utf-8
import json
import uuid
from io import StringIO

import arrow
import autopep8
from django.db import models
from django.urls import reverse

from .base import BaseModel
from .description import Product, ProductInstance, Project


class KeyWord(BaseModel):
    example_code = models.TextField(verbose_name='代码样例')

    class Meta:
        ordering = ('name',)
        verbose_name = '关键字'
        verbose_name_plural = '关键字列表'


class TestItem(BaseModel):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='所属项目')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='所属产品')
    code = models.TextField(verbose_name='测试项代码', help_text='测试项完整python代码')
    parameters = models.TextField(verbose_name='测试项参数', help_text='测试项的参数只要与代码对应，任何格式都可以,由测试项代码直接读取字符串。', blank=True)
    expected = models.TextField(verbose_name='合格判据', blank=True)

    def save(self, *args, **kwargs):
        self.code = autopep8.fix_code(self.code)
        super(TestItem, self).save(*args, **kwargs)

    class Meta:
        ordering = ('name',)
        verbose_name = '测试项'
        verbose_name_plural = '测试项列表'


class Task(BaseModel):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='所属项目')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='所属产品')

    def get_absolute_url(self):
        return reverse('ate_tasks:entity-task-update', kwargs={'pk': self.pk})

    class Meta:
        ordering = ('name',)
        verbose_name = '测试任务'
        verbose_name_plural = '测试任务列表'


class TaskStep(models.Model):
    order = models.IntegerField(verbose_name='执行顺序',
                                help_text='表示测试项在测试任务中的执行顺序')
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='steps')
    test_item = models.ForeignKey(TestItem, on_delete=models.CASCADE, verbose_name='所属测试项')
    uuid = models.UUIDField(verbose_name='步骤ID', unique=True, default=uuid.uuid1)

    @property
    def name(self):
        return '{0}-{1}'.format(self.test_item.name, self.order)

    @property
    def real_name(self):
        return self.test_item.name

    @property
    def expected(self):
        return self.test_item.expected

    def __str__(self):
        return '{0}-{1}'.format(self.test_item.name, self.order)

    @property
    def code(self):
        return self.test_item.code

    @property
    def parameters(self):
        return self.test_item.parameters

    class Meta:
        ordering = ('task', 'order')
        verbose_name = '测试任务步骤'
        verbose_name_plural = '测试任务步骤列表'


class TaskInstance(models.Model):
    creator = models.CharField(max_length=255, verbose_name='创建者')
    created = models.DateTimeField(verbose_name='创建日期', auto_now_add=True)
    modified = models.DateTimeField(verbose_name='修改日期', auto_now=True)
    product_instance = models.ForeignKey(ProductInstance, on_delete=models.CASCADE, verbose_name='所属产品实例')
    uuid = models.UUIDField(verbose_name='实例ID', unique=True, default=uuid.uuid1)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, verbose_name='所属测试任务')
    result = models.TextField(verbose_name='测试结果列表', blank=True, help_text='用于各测试项是否通过。', default='[]')
    detail = models.TextField(verbose_name='任务相关变量明细表', blank=True, help_text='从每一个测试项收集相应的变量，并统一保存在字典里。')

    @property
    def flow_chart_string(self):
        flow_atom = []
        string_io = StringIO()
        steps = self.task.steps.all().order_by('order')
        string_io.write('st=>start: 任务初始化\n')
        string_io.write('e=>end: 任务结束\n')
        if steps.count() > 0:
            for index, step in enumerate(steps):
                string_io.write('op{index}=>operation: {real_name}\n'.format(index=index, real_name=step.real_name))
                flow_atom.append('op{index}'.format(index=index))
            string_io.write('st->{operations}->e\n'.format(operations='->'.join(flow_atom)))
        else:
            string_io.write('st->e\n')
        string_io.seek(0)
        return string_io.read()

    @property
    def name(self):
        return self.task.name

    @property
    def records(self):
        records = json.loads(self.result, encoding='utf-8')
        if not isinstance(records, list):
            raise TypeError('测试记录必须是list类型')
        return records

    @property
    def clean_records(self):
        clean_records = [_ for _ in self.records if _['name'] not in ['start', 'end']]
        return clean_records

    def __str__(self):
        local = arrow.get(self.created).to('Asia/Shanghai')
        return '{name} {time}'.format(name=self.name, time=local.format('YYYY-MM-DD HH:mm:ss'))

    def save_task_detail(self, detail):
        if isinstance(detail, dict):
            self.detail = json.dumps(detail, ensure_ascii=False, indent=4)
            self.save()
        else:
            raise TypeError('必须存入字典')

    def get_record(self, name):
        result = None
        for record in self.records:
            if record.get('name', '') == name:
                result = record
                break
        return result

    def append_test_record(self, record):
        records = self.records
        records.append(record)
        self.result = json.dumps(records, ensure_ascii=False, indent=4)
        self.save()

    class Meta:
        ordering = ('task', 'created')
        verbose_name = '测试任务实例'
        verbose_name_plural = '测试任务实例列表'
