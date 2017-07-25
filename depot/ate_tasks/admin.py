from django.contrib import admin

import ate_tasks.models as models


class BaseAdmin(admin.ModelAdmin):
    list_display = ('name', 'creator', 'created', 'modified', 'description',)
    list_filter = ['created', 'modified', 'creator']
    fieldsets = (
        (None, {
            'fields': ('name', 'creator',)
        }),
        ('选填信息', {
            'classes': ('collapse',),
            'fields': ('description',),
        }),
    )


class ProductAdmin(BaseAdmin):
    list_display = ('name', 'validation_phase', 'project', 'creator', 'description',)
    list_filter = ['validation_phase', 'project', 'creator']
    fieldsets = (
        (None, {
            'fields': ('name', 'validation_phase', 'project', 'creator',)
        }),
        ('选填信息', {
            'classes': ('collapse',),
            'fields': ('description',),
        }),
    )


class ProductInstanceAdmin(BaseAdmin):
    list_display = ('name', 'product', 'creator', 'description',)
    list_filter = ['product', 'creator']
    fieldsets = (
        (None, {
            'fields': ('name', 'product', 'creator',)
        }),
        ('选填信息', {
            'classes': ('collapse',),
            'fields': ('description',),
        }),
    )


class TaskStepInline(admin.TabularInline):
    fields = ['order', 'test_item']
    model = models.TaskStep
    extra = 0


class TaskAdmin(BaseAdmin):
    inlines = [TaskStepInline, ]


class TestItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'project', 'product', 'expected', 'creator', 'created', 'modified', 'description',)
    list_filter = ['created', 'modified', 'creator', 'project', 'product']
    fieldsets = (
        ('辅助信息', {
            'fields': ('name', 'project', 'product', 'creator',)
        }),
        ('关键信息', {
            'fields': ('code', 'parameters', 'expected',),
        }),
        ('选填信息', {
            'classes': ('collapse',),
            'fields': ('description',),
        }),
    )


admin.site.register(models.ValidationPhase, BaseAdmin)
admin.site.register(models.Project, BaseAdmin)
admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.ProductInstance, ProductInstanceAdmin)

admin.site.register(models.TestItem, TestItemAdmin)
admin.site.register(models.Task, TaskAdmin)
admin.site.register(models.TaskInstance)
admin.site.register(models.KeyWord)
admin.site.register(models.ServiceNode)
admin.site.register(models.Device)
admin.site.register(models.BusType)
