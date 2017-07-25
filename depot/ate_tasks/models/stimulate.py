# coding=utf-8
from django.db import models

from .base import BaseModel
from .description import Product, Project


class StimulateSequence(BaseModel):
    content = models.TextField(blank=True, default='[]')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='sequences')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='sequences')

    class Meta:
        ordering = ('name',)
        verbose_name = '激励序列'
        verbose_name_plural = '激励序列列表'
