from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^list/$', views.list, name='list'),
	url(r'^detail/(?P<user>[\w.@+-]+)/(?P<rep>[\w.@+-]+)/$', views.detail, name='detail'),
]