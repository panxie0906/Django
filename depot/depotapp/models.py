# -*- coding=utf-8 -*-
from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=100,verbose_name='产品名称')
    price = models.CharField(max_length=50,verbose_name='产品价格')
    def __unicode__(self):
        return self.name
    class Meta:
        verbose_name = '产品列表'
        verbose_name_plural= '产品清单'