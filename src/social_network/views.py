from httplib import HTTPResponse
import json
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from utils.functions import template, ajax_template, json_response
from social_network.models import Message
from accounts.decorators import user_required
from django.http.response import HttpResponse


@user_required
def userpanel_inbox(request):
    return template(request, 'userpanel/inbox/inbox.html')


@user_required
def userpanel_inbox_list(request):
    messages = request.user.recieved_messages.all()
    return template(request, 'userpanel/inbox/list.html', {'inbox': messages})


@user_required
def userpanel_message(request, message_id):
    message = request.user.recieved_messages.get(pk=message_id)
    message.unread = False ;
    message.save()
    return template(request, 'userpanel/inbox/message.html', {'message': message})


@user_required
def userpanel_send_message(request):
    return template(request, 'userpanel/inbox/send.html')


@csrf_exempt
@user_required
def userpanel_sendEmail(request):
    response = {}
    m = Message()
    m.body = request.POST['recipient']
    m.subject = request.POST['subject']
    m.sender = request.user
    try:
        reciever = User.objects.get(username=request.POST['recipient'])
        m.reciever = reciever
        m.save()
        response['status'] = 'success'
    except:

        response['status'] = 'fail'
        response['error'] = 'invalid username'

    return json_response(response)

def userpanel_friends(request):
    return template(request , 'userpanel/friends.html')
