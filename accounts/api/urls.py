from django.conf.urls import url
import views

app_name = 'accountsapi'

urlpatterns = [
  url(r'^-create/$', views.UserCreateAPIView.as_view(), name = 'apiCreate'),
  url(r'^-mod/$', views.UserListAPIView.as_view(), name = 'apiMod'),
]