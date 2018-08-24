from django.conf.urls import url
import views

app_name = 'accounts'

urlpatterns = [
  url(r'^signup/$', views.signup, name = 'signup'),
  url(r'^profile/$', views.profile, name = 'profile'),
]