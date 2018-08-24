from django.conf.urls import url
import views

app_name = 'blog'

urlpatterns = [
    url(r'^$', views.posts_view, name = 'postlist'),
]