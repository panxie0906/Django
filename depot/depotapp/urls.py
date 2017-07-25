#-*- coding:utf-8 -*-

from django.conf.urls import url,include
#from ..models import models
#用这种..的方式import会报 attempted relative import beyond top-level package
#因为主函数在上级目录中，上级目录尽管有__init__也不被当做package不能用相对路径引用
from .views import views,icd


icd_patterns = [
	url(r'^project/$',icd.IcdProjectListView.as_view(),name='icd-project-list'),
	url(r'^project/upload/$',icd.UploadIcdFormView.as_view(),name='icd-upload'),
	 url(r'^project/(?P<pk>[0-9]+)/$', icd.IcdProjectDetailView.as_view(), name='icd-project-detail'),
    url(r'^project/(?P<pk>[0-9]+)/delete/$', icd.IcdProjectDeleteView.as_view(), name='icd-project-delete'),
    url(r'^query_icd_node_attrs/$', icd.QueryIcdNodeAttrsView.as_view(), name='query-icd-node-attrs'),
]

urlpatterns = [
    url(r'^product/$',views.base_product),
    url(r'^product/create/$', views.create_product),
    url(r'^product/list/$', views.list_product ),
    #url(r'^product/edit/(?P[^/]+)/$', edit_product),
    #url(r'^product/view/(?P[^/]+)/$', view_product),
	url(r'^icd/', include(icd_patterns)),
]