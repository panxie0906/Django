# coding=utf-8
from django.db import models

from .base import BaseModel


class Project(BaseModel):
    class Meta:
        ordering = ('name',)
        verbose_name = '项目'
        verbose_name_plural = '项目列表'


class ValidationPhase(BaseModel):
    class Meta:
        ordering = ('name',)
        verbose_name = '验证阶段'
        verbose_name_plural = '验证阶段列表'


class Product(BaseModel):
    validation_phase = models.ForeignKey(ValidationPhase, on_delete=models.CASCADE, verbose_name='验证阶段')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='所属项目')
    img = models.ImageField(verbose_name='缩略图', blank=True, upload_to='img')

    class Meta:
        ordering = ('name',)
        verbose_name = '产品'
        verbose_name_plural = '产品列表'


class ProductInstance(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='所属产品')

    class Meta:
        ordering = ('name',)
        verbose_name = '产品实例'
        verbose_name_plural = '产品实例列表'
