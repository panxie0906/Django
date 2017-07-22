from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from . import views
from .views.auth import *

app_name ='polls'

router = DefaultRouter()
router.register(r'views',views.TaskInstanceViewSet)

auth_patterns = [
    url(r'login/$',LoginView.as_view(),name='login'),
    url(r'logout/$',LogoutView.as_view(),name='logout'),
]

urlpatterns = [
    # ex: /polls/
    url(r'^$', views.index, name='index'),
	#show time
	url(r'^time$',views.showtime),
    # ex: /polls/5/
    url(r'^(?P<question_id>[0-9]+)/$', views.detail, name='detail'),
    # ex: /polls/5/results/
    url(r'^(?P<question_id>[0-9]+)/results/$', views.results, name='results'),
    # ex: /polls/5/vote/
    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
]+auth_patterns