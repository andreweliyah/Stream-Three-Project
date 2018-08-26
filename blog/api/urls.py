from django.conf.urls import url
import views

app_name = 'blogapi'
urlpatterns = [
  url(r'^$', views.PostAPIView.as_view(), name = 'list'),
]