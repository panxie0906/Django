# coding=utf-8
from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'ate_tasks'
router = DefaultRouter()
router.register(r'validation_phase', views.ValidationPhaseViewSet)
router.register(r'project', views.ProjectViewSet)
router.register(r'product', views.ProductViewSet)
router.register(r'product_instance', views.ProductInstanceViewSet)
router.register(r'keyword', views.KeyWordViewSet)
router.register(r'test_item', views.TestItemViewSet)
router.register(r'task', views.TaskViewSet)
router.register(r'task_instance', views.TaskInstanceViewSet)
api_patterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
auth_patterns = [
    url(r'^login/$', views.LoginView.as_view(), name='login'),
    url(r'^logout/$', views.LogoutView.as_view(), name='logout'),
]

runner_patterns = [
    url(r'^$', views.ShowRunnerView.as_view(), name='execute-runner-list'),
    url(r'^runner/(?P<pk>[0-9]+)/$', views.TaskRunnerView.as_view(),
        name='execute-runner'),
    url(r'^result/(?P<pk>[0-9]+)/$', views.get_instance_result,
        name='execute-task-instance-result'),
    url(r'^runner/(?P<pk>[0-9]+)/run/$', views.run_task_instance, name='run_task_instance'),
    url(r'^runner/(?P<pk>[0-9]+)/suspend/$', views.suspend_task, name='suspend-task-instance'),
]
icd_patterns = [
    url(r'^project/$', views.IcdProjectListView.as_view(), name='icd-project-list'),
    url(r'^project/upload/$', views.UploadIcdFormView.as_view(), name='icd-upload'),
    url(r'^project/(?P<pk>[0-9]+)/$', views.IcdProjectDetailView.as_view(), name='icd-project-detail'),
    url(r'^project/(?P<pk>[0-9]+)/delete/$', views.IcdProjectDeleteView.as_view(), name='icd-project-delete'),
    url(r'^query_icd_node_attrs/$', views.QueryIcdNodeAttrsView.as_view(), name='query-icd-node-attrs'),

]
device_patterns = [
    url(r'^list/(?P<pk>[0-9]+)/$', views.DeviceMessageBindingView.as_view(), name='device-message-binding'),
    url(r'^list/$', views.DeviceListView.as_view(), name='device-list'),
    url(r'^list/update/$', views.DeviceUploadView.as_view(), name='device-upload'),
]
test_patterns = [
    url(r'^form_test/(?P<pk>[0-9]+)/$', views.form_test, name='form-test'),
    url(r'^config_test/$', views.config_test, name='config-test'),
    url(r'^icd_upload_test/$', views.UploadIcdFormView.as_view(), name='icd-upload-test'),
    url(r'^fancy_tree_test/$', views.fancy_tree_test, name='fancy-tree-test'),
]
monitor_patterns = [
    url(r'^new/$', views.NewMonitorView.as_view(), name='monitor-new'),
    url(r'^(?P<pk>[0-9]+)/$', views.MonitorDetailView.as_view(), name='monitor-detail'),
    url(r'^set_rule/(?P<pk>[0-9]+)/$', views.SetMonitorFilterRule.as_view(), name='monitor-set-rule'),
]
stimulate_patterns = [
    url(r'^$', views.StimulateIndex.as_view(), name='stimulate-index'),
    url(r'^execute/single/$', views.StimulateSingleMessage.as_view(), name='stimulate-execute-single-message'),
]
data_patterns = [
    url(r'^get_tree/$', views.GetTreeView.as_view(), name='get-tree'),
    url(r'^get_binding_schema/$', views.GetBusTypeBindingSchema.as_view(), name='get-binding-schema'),
    url(r'^get_message_schema/$', views.GetBusTypeMessageSchema.as_view(), name='get-message-schema'),
    url(r'^get_binding_option/$', views.GetBusTypeBindingOption.as_view(), name='get-binding-option'),
    url(r'^get_message_option/$', views.GetBusTypeMessageOption.as_view(), name='get-message-option'),
    url(r'^get_device_binding/$', views.GetDeviceBinding.as_view(), name='get-device-binding'),
    url(r'^get_random_message_init_data/$', views.GetRandomMessageInitData.as_view(),
        name='get-random-message-init-data'),
]


def get_entity_patterns(generator, entity_pattern_name):
    patterns = [
        url(r'^$', generator.get_list_view().as_view(),
            name='entity-{pattern_name}-list'.format(pattern_name=entity_pattern_name)),
        url(r'^create/$', generator.get_create_view().as_view(),
            name='entity-{pattern_name}-create'.format(pattern_name=entity_pattern_name)),
        url(r'^update/(?P<pk>[0-9]+)/$', generator.get_update_view().as_view(),
            name='entity-{pattern_name}-update'.format(pattern_name=entity_pattern_name)),
        url(r'^delete/(?P<pk>[0-9]+)/$', generator.get_delete_view().as_view(),
            name='entity-{pattern_name}-delete'.format(pattern_name=entity_pattern_name))
    ]
    return patterns


entity_patterns = [
    url(r'^validation_phase/', include(get_entity_patterns(views.ValidationPhaseViewGenerator, 'validation-phase'))),
    url(r'^test_item/', include(get_entity_patterns(views.TestItemViewGenerator, 'test-item'))),
    url(r'^task/', include(get_entity_patterns(views.TaskViewGenerator, 'task'))),
    url(r'^project/', include(get_entity_patterns(views.ProjectViewGenerator, 'project'))),
    url(r'^product/', include(get_entity_patterns(views.ProductViewGenerator, 'product'))),
    url(r'^product_instance/', include(get_entity_patterns(views.ProductInstanceViewGenerator, 'product-instance'))),
    url(r'^keyword/', include(get_entity_patterns(views.KeywordViewGenerator, 'keyword'))),
    url(r'^task_instance/', include(get_entity_patterns(views.TaskInstanceViewGenerator, 'task-instance')))
]

urlpatterns = [
    url(r'^$', views.Index.as_view(), name='index'),
    url(r'^auth/', include(auth_patterns)),
    url(r'^api/', include(api_patterns)),
    url(r'^entity/', include(entity_patterns)),
    url(r'^execute/', include(runner_patterns)),
    url(r'^icd/', include(icd_patterns)),
    url(r'^device/', include(device_patterns)),
    url(r'^monitor/', include(monitor_patterns)),
    url(r'^stimulate/', include(stimulate_patterns)),
    url(r'^test/', include(test_patterns)),
    url(r'^data/', include(data_patterns)),
]
