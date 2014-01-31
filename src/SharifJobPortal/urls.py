from django.conf.urls 	import patterns, include, url
from django.contrib 	import admin
from django.conf        import settings
from SharifJobPortal.views import index
from utils.views        import zedit_preview
from ui_test.views 		import show_template
from accounts.views     import profile_employer, profile_jobseeker, profile_employer_comments
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
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    
    url(r'^employer/(?P<username>\w+)/', profile_employer),
    url(r'^comments/employer/(?P<employer_id>\w+)/', profile_employer_comments),

    url(r'^user/(?P<username>\w+)/', profile_jobseeker),

	url(r'^ajax/(?P<template>(\w|[/])+)/$', show_template),
	url(r'^(?P<template>\w+)/$', show_template),
)

