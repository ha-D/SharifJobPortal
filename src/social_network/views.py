from django.shortcuts 		import render_to_response
from utils.functions		import template, ajax_template
from social_network.models 	import Message
from accounts.decorators	import user_required_ajax

@user_required_ajax
def userpanel_inbox(request):
	return ajax_template(request, 'userpanel/inbox/inbox.html')

@user_required_ajax
def userpanel_inbox_list(request):
	messages = request.user.recieved_messages.all()
	return ajax_template(request, 'userpanel/inbox/list.html', {'inbox': messages})

@user_required_ajax
def userpanel_message(request, message_id):
	message = request.user.recieved_messages.get(pk = message_id)
	return ajax_template(request, 'userpanel/inbox/message.html', {'message': message})

@user_required_ajax
def userpanel_send_message(request):
	return ajax_template(request, 'userpanel/inbox/send.html')