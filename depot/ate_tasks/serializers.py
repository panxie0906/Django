# coding=utf-8
from rest_framework import serializers

import ate_tasks.models as models


class ValidationPhaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ValidationPhase
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Project
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = '__all__'


class ProductInstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductInstance
        fields = '__all__'


class KeyWordSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.KeyWord
        fields = '__all__'


class TestItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TestItem
        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Task
        fields = '__all__'


class TaskInstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TaskInstance
        fields = ('uuid', 'created', 'modified', 'creator', 'name', 'records')
