from django.conf.urls import patterns, url
from jobs.views import applyJob, refuseJob, acceptOffer, rejectOffer, deleteJob, editJob, newJob, jobPage

urlpatterns = patterns('',
    url(r'apply/(?P<jobid>\d+)$', applyJob),
    url(r'^refuse/(?P<jobid>\d+)$', refuseJob),
    url(r'^delete/(?P<jobid>\d+)$', deleteJob),
    url(r'^edit/(?P<jobid>\d+)/$', editJob),
    url(r'^new/$', newJob),
    url(r'^offers/accept/(?P<offerid>\d+)$', acceptOffer),
    url(r'^offers/reject/(?P<offerid>\d+)$', rejectOffer),
    url(r'^(?P<jobid>\d+)/$', jobPage),
)
