from django.conf.urls 	import patterns, include, url
from django.contrib 	import admin

from ui_test.views 		import show_template
from accounts.views		import register_jobseeker

# Uncomment the next two lines to enable the admin:
admin.autodiscover()


urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),

    url(r'^register/(?P<action>\w+)', register_jobseeker),

	url(r'^ajax/(?P<template>(\w|[/])+)/$', show_template),
	url(r'^(?P<template>\w+)/', show_template),
	
    # Examples:
    # url(r'^$', 'SharifJobPortal.views.home', name='home'),
    # url(r'^SharifJobPortal/', include('SharifJobPortal.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
)
