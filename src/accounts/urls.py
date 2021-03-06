from django.conf.urls 			import patterns, url
from django.contrib.auth.models import User
from accounts.views 			import mylogin, mylogout
from accounts.register 			import register_employer, register_jobseeker, register_jobseeker_skills_handle

urlpatterns = patterns('',
	url(r'^register/jobseeker/skills/handle/', register_jobseeker_skills_handle),
	url(r'^register/jobseeker/(?P<action>\w*)', register_jobseeker),
    url(r'^register/employer/(?P<action>\w*)', register_employer),
    url(r'^login/$', mylogin),
    url(r'^logout/$', mylogout),
)
