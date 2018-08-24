from django.conf.urls import url
import views

app_name = 'blogapi'
urlpatterns = [
  # url(r'^users/$', views.UserListAPIView.as_view(), name = 'apilist'),
  url(r'^$', views.PostListAPIView.as_view(), name = 'apilist'),
]