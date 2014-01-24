from django.conf.urls import patterns, url
from jobs.views import applyJob, refuseJob, acceptOffer, rejectOffer

urlpatterns = patterns('',
    url(r'apply/(?P<jobid>\d+)$', applyJob),
    url(r'^refuse/(?P<jobid>\d+)$', refuseJob),
    url(r'^offers/accept/(?P<offerid>\d+)$', acceptOffer),
    url(r'^offers/reject/(?P<offerid>\d+)$', rejectOffer),
)
