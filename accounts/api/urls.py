from django.conf.urls import url
import views

app_name = 'accountsapi'

urlpatterns = [
  url(r'^-auth/$', views.UserAuthAPIView.as_view(), name = 'auth'),
  url(r'^-payments/$', views.PaymentAPIView.as_view(), name = 'payment'),
]