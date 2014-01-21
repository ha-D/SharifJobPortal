from django.shortcuts 		import render_to_response
from utils.functions		import template, ajax_template
from social_network.models 	import Message
from accounts.decorators	import user_required

@user_required
def userpanel_inbox(request):
	return template(request, 'userpanel/inbox/inbox.html')

@user_required
def userpanel_inbox_list(request):
	messages = request.user.recieved_messages.all()
	return template(request, 'userpanel/inbox/list.html', {'inbox': messages})

@user_required
def userpanel_message(request, message_id):
	message = request.user.recieved_messages.get(pk = message_id)
	return template(request, 'userpanel/inbox/message.html', {'message': message})

@user_required
def userpanel_send_message(request):
	return template(request, 'userpanel/inbox/send.html')