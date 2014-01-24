from django.conf.urls 			import patterns, url
from django.contrib.auth.models import User
from accounts.views				import userpanel_main, userpanel_jobs
from social_network.views 		import userpanel_inbox, userpanel_inbox_list, userpanel_message, userpanel_send_message

urlpatterns = patterns('',
	url(r'^$', userpanel_main),
	url(r'^inbox/(?P<message_id>\d+)/$', userpanel_message),
	url(r'^inbox/send/$', userpanel_send_message),
	url(r'^inbox/list/$', userpanel_inbox_list),
	url(r'^inbox/$', userpanel_inbox),
    url(r'^jobs/$', userpanel_jobs),
)
