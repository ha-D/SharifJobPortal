from django.conf.urls 			import patterns, url
from django.contrib.auth.models import User
from accounts.views				import *
from social_network.views 		import *

urlpatterns = patterns('',
	url(r'^$', userpanel_main),
	url(r'^inbox/(?P<message_id>\d+)/$', userpanel_message),
	url(r'^inbox/send/$', userpanel_send_message),
	url(r'^inbox/list/$', userpanel_inbox_list),
	url(r'^inbox/$', userpanel_inbox),
	url(r'^inbox/send/sendEmail', userpanel_sendEmail),

	url(r'^friends/$', userpanel_friends),
	url(r'friends/search$', userpanel_searchFriend),
	url(r'friends/requestFriendShip$' , userpanel_requestFriendShip),
	# url(r'friends/requestFriendShip11$' , userpanel_requestFriendShip),
    url(r'friends/responseToFriendShip' , userpanel_responseToFriendShip),


	url(r'^jobs/$', userpanel_jobs),
	url(r'^offers/$', userpanel_offers),

	
	url(r'^profile/$', userpanel_changeinfo),
	url(r'^companyinfo/$', userpanel_changecompanyinfo),
	url(r'^companyinfo/uploadimage/$', userpanel_changecompanyinfo_uploadimage),
	url(r'^companyinfo/removeimage/(?P<image_id>\d+)$', userpanel_changecompanyinfo_removeimage),
	url(r'^companyinfo/zedit/$', userpanel_info_profile_pages),

	url(r'^info/skills/$', userpanel_changejobseekerinfo_skills),
	url(r'^info/privacy/$', userpanel_changejobseekerinfo_privacy),
)
