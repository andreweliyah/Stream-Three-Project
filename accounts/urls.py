from django.conf.urls import url
import views

app_name = 'accounts'

urlpatterns = [
  url(r'^signup/$', views.signup, name = 'signup'),
  url(r'^profile/$', views.profile, name = 'profile'),
  url(r'^login/$', views.login, name = 'login'),
  url(r'^logout/$', views.logout, name = 'logout'),
  url(r'^settings/', views.settings, name='settings'),
  url(r'^delete/', views.delete, name='delete'),
]