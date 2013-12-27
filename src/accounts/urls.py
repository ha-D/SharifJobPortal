from django.conf.urls import patterns, url
from django.contrib.auth.models import User
from accounts.views import mylogin, mylogout

urlpatterns = patterns('',
    url(r'^login/$', mylogin),
    url(r'^logout/$', mylogout),
)
