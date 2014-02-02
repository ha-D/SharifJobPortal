from django.conf.urls 	import patterns, include, url
from django.contrib 	import admin
from django.conf        import settings
from SharifJobPortal.views import index
from utils.views        import zedit_preview
from ui_test.views 		import show_template
from accounts.views     import *
from jobs.views         import *
import userpanel_urls

# Uncomment the next two lines to enable the admin:
admin.autodiscover()

urlpatterns = patterns('')

if settings.DEBUG:
    urlpatterns += patterns('',
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}))


urlpatterns += patterns('',
    url(r'^$', index),
    url(r'^zedit/preview/$', zedit_preview),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^userpanel/',  include(userpanel_urls)),

    url(r'^accounts/', include('accounts.urls')),

    url(r'^search/', include('search.urls')),
    url(r'^jobs/', include('jobs.urls')),
    
    url(r'^employer/(?P<username>\w+)/', profile_employer),
    url(r'^user/(?P<username>\w+)/', profile_jobseeker),
    
    url(r'^comments/employer/(?P<employer_id>\d+)/', profile_employer_comments),
    url(r'^rate/employer/(?P<employer_id>\d+)/', profile_employer_rate),
    url(r'^comments/job/(?P<job_id>\d+)/', job_comment),
    url(r'^rate/job/(?P<job_id>\d+)/', job_rate),


    url(r'^cv/(?P<jobseeker_id>\d+)/', profile_jobseeker_getcv),

    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
	# url(r'^ajax/(?P<template>(\w|[/])+)/$', show_template),
	# url(r'^(?P<template>\w+)/$', show_template),
)

