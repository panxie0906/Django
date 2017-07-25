# coding=utf-8
from django.db import models


class Permission(models.Model):
    class Meta:
        permissions = (
            ("ate_validation_phase", "验证阶段管理"),
            ("ate_project", "项目管理"),
            ("ate_product", "产品管理"),
            ("ate_product_instance", "产品实例管理"),
            ("ate_test_item", "测试项管理"),
            ("ate_tasks", "测试任务管理"),
        )
