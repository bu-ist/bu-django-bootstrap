from django.conf.urls import patterns, url, include
import views

urlpatterns = patterns('',
    # Examples:
    url(r'^$', views.home, name='home'),
)
