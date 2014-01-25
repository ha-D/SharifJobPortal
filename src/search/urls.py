from django.conf.urls import patterns, url
from views import opSearch, userSearch, skillSearch, updateRate

urlpatterns = patterns('',
	url(r'^$', opSearch),
	url(r'^op/$', opSearch),
    url(r'^user$', userSearch),
    url(r'^skill/$', skillSearch),
    url(r'^rate/$', updateRate),
)
