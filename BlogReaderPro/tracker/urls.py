from django.conf.urls import url
from . import views

app_name='tracker'

urlpatterns = [
  url(r'^$', views.index, name='index'),
  url(r'^form', views.form, name='form'),
  url(r'^ticket-(?P<id>\d+)/$', views.ticket, name='ticket'),
]