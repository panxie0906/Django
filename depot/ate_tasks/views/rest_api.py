# coding=utf-8

from rest_framework import viewsets

import ate_tasks.models as models
import ate_tasks.serializers as serializers


class ValidationPhaseViewSet(viewsets.ModelViewSet):
    queryset = models.ValidationPhase.objects.all()
    serializer_class = serializers.ValidationPhaseSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = models.Project.objects.all()
    serializer_class = serializers.ProjectSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer


class ProductInstanceViewSet(viewsets.ModelViewSet):
    queryset = models.ProductInstance.objects.all()
    serializer_class = serializers.ProductInstanceSerializer


class KeyWordViewSet(viewsets.ModelViewSet):
    queryset = models.KeyWord.objects.all()
    serializer_class = serializers.KeyWordSerializer


class TestItemViewSet(viewsets.ModelViewSet):
    queryset = models.TestItem.objects.all()
    serializer_class = serializers.TestItemSerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = models.Task.objects.all()
    serializer_class = serializers.TaskSerializer


class TaskInstanceViewSet(viewsets.ModelViewSet):
    queryset = models.TaskInstance.objects.all()
    serializer_class = serializers.TaskInstanceSerializer
