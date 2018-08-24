from django.conf.urls import url
import views

app_name = 'blog'

urlpatterns = [
    url(r'^$', views.posts_view, name = 'postlist'),
    url(r'^(?P<id>\d+)/edit$', views.edit_post, name='editpost'),
    url(r'^newpost/$', views.new_post, name='newpost'),
    url(r'^post-(?P<id>\d+)/$', views.post_detail, name='postdetail'),

]