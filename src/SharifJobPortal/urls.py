from django.conf.urls 	import patterns, include, url
from django.contrib 	import admin
from django.conf import settings

from ui_test.views 		import show_template
from accounts.views		import userpanel

import userpanel_urls

# Uncomment the next two lines to enable the admin:
admin.autodiscover()


urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    
    url(r'^userpanel/',  include(userpanel_urls)),

    url(r'^accounts/', include('accounts.urls')),

    url(r'^search/', include('search.urls')),    
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    
	url(r'^ajax/(?P<template>(\w|[/])+)/$', show_template),
	url(r'^(?P<template>\w+)/', show_template),
	
    # Examples:
    # url(r'^$', 'SharifJobPortal.views.home', name='home'),
    # url(r'^SharifJobPortal/', include('SharifJobPortal.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
)

# if settings.DEBUG:
#     # static files (images, css, javascript, etc.)
#         urlpatterns += patterns('',
#             (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
#             'document_root': settings.MEDIA_ROOT}))

