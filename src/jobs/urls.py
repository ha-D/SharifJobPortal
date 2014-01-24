from django.conf.urls import patterns, url
from jobs.views import applyJob, refuseJob

urlpatterns = patterns('',
    url(r'apply/(?P<jobid>\d+)$', applyJob),
    url(r'^refuse/(?P<jobid>\d+)$', refuseJob),
)
