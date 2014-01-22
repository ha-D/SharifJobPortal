from django.conf.urls import patterns, url
from views import opSearch, userSearch, skillSearch

urlpatterns = patterns('',
	url(r'^$', opSearch),
	url(r'^op/$', opSearch),
    url(r'^user/$', userSearch),
    url(r'^skill/$', skillSearch),
)
