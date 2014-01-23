from django.contrib.auth.views 		import login, logout
from django.shortcuts            	import render, render_to_response
from django.template             	import RequestContext
from django.template.loader     	import render_to_string
from django.http                 	import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models 	import User
from utils.functions		 		import template, json_response, ajax_template
from accounts.decorators 			import user_required
from accounts.forms                	import *
from django.conf 					import settings

def mylogin(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)
    if request.method == 'POST':
        if not request.POST.get('remember_me', None):
            request.session.set_expiry(0)
    return login(request, template_name='accounts/login.html')


def mylogout(request):
    return logout(request, next_page=settings.LOGOUT_REDIRECT_URL)

@user_required
def userpanel_main(request):
    print(type(request.userprofile))
    if request.userprofile.is_jobseeker():
        return template(request, 'userpanel/jobseeker/main.html')
    elif request.userprofile.is_employer():
        return template(request, 'userpanel/employer/main.html')

@user_required
def userpanel_changeinfo(request):
    if request.method == 'POST':
        form = ChangeUserInfoForm(request.POST)
        if form.is_valid():
            return HttpResponse("OK")
    else:
        form = ChangeUserInfoForm(instance = request.user)
    
    return render(request, 'userpanel/changeuserinfo.html', {'form': form})