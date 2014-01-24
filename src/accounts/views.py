from django.contrib.auth.views 		import login, logout
from django.shortcuts            	import render, render_to_response
from django.template             	import RequestContext
from django.template.loader     	import render_to_string
from django.http                 	import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models 	import User
from django.views.decorators.csrf   import csrf_exempt
from django.conf 					import settings

from utils.functions                import template, json_response, ajax_template
from accounts.decorators            import user_required, employer_required, jobseeker_required
from accounts.models                import CompanyImage, PersonalPage
from accounts.forms                 import *

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


@user_required #OBSOLETE
def userpanel_changeinfo_old(request):
    context = {}
    if request.method == 'POST':
        form = ChangeUserInfoForm(request.POST, request.FILES, instance=request.userprofile)
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
        userform = ChangeUserInfoForm(request.POST, request.FILES, instance=request.userprofile)
        compform = ChangeCompanyInfoForm(request.POST, instance=request.userprofile)
        if userform.is_valid() and compform.is_valid():
            userform.save()
            compform.save()
            context['state'] = 'success'
        else:
            print(compform.errors)
            print(userform.errors)
            print("SHIT")
    else:
        userform = ChangeUserInfoForm(instance = request.userprofile)
        compform = ChangeCompanyInfoForm(instance = request.userprofile)

    context['images'] = list(request.userprofile.images.all())
    context['compform'] = compform
    context['userform'] = userform

    return render(request, 'userpanel/employer/changecompanyinfo.html', context)


@user_required
def userpanel_changeinfo(request):
    if request.userprofile.is_employer():
        return userpanel_changecompanyinfo(request)
    else:
        return userpanel_changejobseekerinfo(request)

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


@csrf_exempt
def userpanel_changecompanyinfo_zedit(request):
    action = request.POST.get('action', '')

    try:
        if action == 'save':
            page_id = request.POST['page_id']
            content = request.POST['content']

            page = PersonalPage.objects.get(pk = page_id)
            if page.user != request.user:
                raise "Unauthorized"
            page.content = content
            page.save()

            return json_response({'result': 'success'})

        elif action == 'remove':
            page_id = request.POST['page_id']

            page = PersonalPage.objects.get(pk = page_id)
            if page.user != request.user:
                raise "Unauthorized"
            page.delete()

            return json_response({'result': 'success'})

        elif action == 'add':
            title = request.POST['title']
            page = PersonalPage.objects.create(user=request.user, title=title)
            page = {'page_id': page.id, 'title':page.title, 'content': page.content}
            return json_response({'result': 'success', 'page': page})

        elif action == 'list':
            pages = PersonalPage.objects.filter(user=request.user)
            pages = map(lambda x: {'page_id': x.id, 'title':x.title, 'content': x.content}, pages)
            return json_response({'result': 'success', 'pages': pages})

    except NameError as e:
        print(e)
        return json_response({'result': 'fail'})