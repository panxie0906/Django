# coding=utf-8
import uuid

from django.db import models


class Monitor(models.Model):
    uuid = models.UUIDField(verbose_name='监控ID号', unique=True, default=uuid.uuid1)
    rules = models.TextField(blank=True, verbose_name='订阅规则')
    is_running = models.BooleanField(default=False, verbose_name='是否正在运行')


class MonitorRecord(models.Model):
    created = models.DateTimeField(verbose_name='创建日期', auto_now_add=True)
    content = models.TextField()
