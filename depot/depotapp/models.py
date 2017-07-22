# -*- coding=utf-8 -*-
from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=100,verbose_name='产品名称')
    price = models.CharField(max_length=50,verbose_name='产品价格')