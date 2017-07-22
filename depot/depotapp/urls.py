from django.conf.urls import url
from .models import *
from .views import *


urlpatterns = [
    url(r'^product/$',base_product),
    url(r'^product/create/$', create_product),
    url(r'^product/list/$', list_product ),
    #url(r'^product/edit/(?P[^/]+)/$', edit_product),
    #url(r'^product/view/(?P[^/]+)/$', view_product),
]