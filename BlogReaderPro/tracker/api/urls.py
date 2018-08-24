from django.conf.urls import url
import views

app_name='trackerapi'

urlpatterns = [
  # url(r'^-list/$', views.TicketListAPIView.as_view(), name = 'apilist'),
  # url(r'^-mod/$', views.TicketModAPIView.as_view(), name = 'apiMod'),
  url(r'^vote/$', views.VoteAPI.as_view(), name = 'vote'),
  url(r'^comment/$', views.CommentAPI.as_view(), name = 'comment'),
  url(r'^ticket/$', views.TicketAPI.as_view(), name = 'ticket'),
]