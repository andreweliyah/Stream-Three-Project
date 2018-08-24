from django.conf.urls import url
import views

urlpatterns = [
  url(r'^-create/$', views.UserCreateAPIView.as_view(), name = 'apiCreate'),
  url(r'^-mod/$', views.UserListAPIView.as_view(), name = 'apiMod'),
  # url(r'^-pay/$', views.UserPaymentAPIView.as_view(), name = 'apiPay')
]