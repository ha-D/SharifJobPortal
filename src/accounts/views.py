from django.contrib.auth.views 		import login, logout
from django.shortcuts            	import render, render_to_response
from django.template             	import RequestContext
from django.template.loader     	import render_to_string
from django.http                 	import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models 	import User
from utils.functions		 		import template, json_response, ajax_template
from accounts.decorators 			import user_required, employer_required, jobseeker_required
from accounts.models                import CompanyImage
from accounts.forms                	import *
from django.conf 					import settings
from django.views.decorators.csrf   import csrf_exempt

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
    context = {}
    if request.method == 'POST':
        form = ChangeUserInfoForm(request.POST, instance=request.userprofile)
        if form.is_valid():
            form.save()
            context['state'] = 'success'
    else:
        form = ChangeUserInfoForm(instance = request.userprofile)

    context['form'] = form
    return render(request, 'userpanel/changeuserinfo.html', context)

@employer_required
def userpanel_changecompanyinfo(request):
    context = {}
    if request.method == 'POST':
        form = ChangeCompanyInfoForm(request.POST, instance=request.userprofile)
        if form.is_valid():
            form.save()
            context['state'] = 'success'
    else:
        form = ChangeCompanyInfoForm(instance = request.userprofile)
    context['images'] = list(request.userprofile.images.all())
    context['form'] = form
    return render(request, 'userpanel/employer/changecompanyinfo.html', context)

@csrf_exempt
def userpanel_changecompanyinfo_uploadimage(request):
    if request.method == 'POST':
        form = CompanyImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            images_count = len(request.userprofile.images.all())
            if images_count >= 5:
                return json_response({'result': 'fail', 'error': 'maximum reached'})            

            comp_image = form.save(commit=False)
            comp_image.employer = request.userprofile
            comp_image.save()

            images = request.userprofile.images.all()
            images = map(lambda x: {'id': x.id, 'url': x.image.url}, images)
            return json_response({'result': 'success', 'images': images})
        else:
            return json_response({'result': 'fail', 'error': 'invalid form'})
    return json_response({'result': 'fail', 'error': 'get not supported'})


@employer_required
@csrf_exempt
def userpanel_changecompanyinfo_removeimage(request, image_id):
    try:
        comp_image = CompanyImage.objects.get(pk = image_id)
    except:
        return json_response({'result': 'fail', 'error': 'invalid id'})

    if comp_image.employer != request.userprofile:
        return json_response({'result': 'fail', 'error': 'not authorized to delete this image'})        

    comp_image.delete()

    images = request.userprofile.images.all()
    images = map(lambda x: {'id': x.id, 'url': x.image.url}, images)
    return json_response({'result': 'success', 'images': images})