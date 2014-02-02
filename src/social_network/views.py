from django.contrib.auth.models     import User
from django.db.models.query_utils   import Q
from django.shortcuts               import render_to_response
from django.views.decorators.csrf   import csrf_exempt
from django.http.response           import HttpResponse

from accounts.models                import JobSeeker
from social_network.functions import friends
from utils.functions                import template, ajax_template, json_response
from social_network.models          import *
from accounts.decorators            import user_required
from social_network.functions       import friends

import json

@user_required
def userpanel_inbox(request):
    return template(request, 'userpanel/inbox/inbox.html')


@user_required
def userpanel_inbox_list(request):
    messages = request.user.recieved_messages.all()
    print(request.user)
    print(messages)
    return template(request, 'userpanel/inbox/list.html', {'inbox': messages})


@user_required
def userpanel_message(request, message_id):
    message = request.user.recieved_messages.get(pk=message_id)
    message.unread = False
    message.save()
    return template(request, 'userpanel/inbox/message.html', {'message': message})


@user_required
def userpanel_send_message(request):
    receiver = request.GET.get('to', None)
    return template(request, 'userpanel/inbox/send.html', {'receiver': receiver})


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
    friends = [fs.jobSeeker2 for fs in JobSeeker.objects.get(user=request.user).requestedFriendShips.filter(status=FriendShip.ACCEPTED)]
    friends.extend([fs.jobSeeker1 for fs in JobSeeker.objects.get(user=request.user).invitedFriendShips.filter(status=FriendShip.ACCEPTED)])

    pending_friends = [fs.jobSeeker1 for fs in JobSeeker.objects.get(user=request.user).invitedFriendShips.filter(status=FriendShip.PENDING)]
    print('pending freinds: ')
    print(pending_friends)
    return template(request, 'userpanel/friends.html', {'friends': friends , 'pending_friends' : pending_friends})


@csrf_exempt
def userpanel_searchFriend(request):
    names = (request.GET['name']).split(' ')
    print(names)
    myfriends = set()
    for name in names:
        query = (Q(user__first_name__contains=name) | Q(user__last_name__contains=name))&~Q(user = request.user)
        retrieved = JobSeeker.objects.filter(query)
        myfriends.update(set(retrieved))

    def getJobSeeker(user1):
        return JobSeeker.objects.get(user = user1)

    # k = [ { 'sa' : 1 } for f in friends]

    friendsList = [{'pic': f.image.url ,
                    'name': '%s %s' % (f.user.first_name, f.user.last_name),
                    'id' : f.id ,
                    'isFriend' : friends(getJobSeeker(request.user) , f)}
                   for f in list(myfriends)]
    friendsList = sorted(friendsList, key=lambda f: not f['isFriend'])
    # return json_response({'friends' : friendsList})
    return HttpResponse(json.dumps({'friends' : friendsList}), content_type="application/json")


@csrf_exempt
def userpanel_responseToFriendShip(request):
    print('swer are here')
    friendID=int(request.POST['friendID'])
    rstatus = request.POST['accepted']
    print(rstatus)
    print(request.POST['accepted'])
    if rstatus == 'false':
        rstatus = False
    else:
        rstatus = True

    print(friendID )
    print(rstatus)
    offerer = JobSeeker.objects.get(pk = friendID)
    fs = list(FriendShip.objects.filter(jobSeeker1 = offerer , jobSeeker2 = JobSeeker.objects.get(pk=request.user.id)))
    fs.extend(FriendShip.objects.filter(jobSeeker2 = offerer , jobSeeker1 = JobSeeker.objects.get(pk=request.user.id)))
    fs = fs[0]
    if rstatus:
        fs.status = FriendShip.ACCEPTED
        fs.save()
    else:
        fs.delete()
    return HttpResponse(json.dumps({'status':'success' , 'image':offerer.image.url , 'name' : offerer.full_name}), content_type="application/json")





@csrf_exempt
def userpanel_requestFriendShip(request):
    invited_user_id = request.POST['invitedUser']
    user1 = JobSeeker.objects.get(user = request.user)
    print(user1)
    user2 = JobSeeker.objects.get(id = invited_user_id)
    print(user2)
    friendShip = FriendShip(jobSeeker1=user1 , jobSeeker2=user2)
    friendShip.save()
    print('friendship successfuly sabt shod :D ')
    return json_response(({'status' : 'you have successfully invited  "' + user2.full_name + '"  to be your friend.'}))

