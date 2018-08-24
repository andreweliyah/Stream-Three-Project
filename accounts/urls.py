from django.conf.urls import url
import views

app_name = 'accounts'

urlpatterns = [
  url(r'^signup/$', views.signup, name = 'signup'),
  url(r'^profile/$', views.profile, name = 'profile'),
  url(r'^logout/$', views.logout, name='logout'),
  url(r'^login/$', views.login, name = 'login'),
  url(r'^settings/', views.settings, name='settings'),
  url(r'^payments/', views.payments),
  url(r'^delete/', views.delete, name='delete'),
  url(r'^cancel_subscription/$', views.cancel_subscription, name='cancel'),
]