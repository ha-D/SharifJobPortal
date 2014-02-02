#coding=utf-8
from _csv import Error

from django.contrib.auth.views 		import login, logout
from django.shortcuts            	import render, render_to_response
from django.template             	import RequestContext
from django.template.loader     	import render_to_string
from django.http                 	import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth.models 	import User
from django.views.decorators.csrf   import csrf_exempt
from django.utils.safestring        import SafeText
from django.core.paginator          import Paginator
from django.core.exceptions         import PermissionDenied
from django.conf 					import settings
from django.views.static            import serve

from utils.functions                import template, json_response, ajax_template
from accounts.decorators            import user_required, employer_required, jobseeker_required
from accounts.models                import CompanyImage, PersonalPage, Employer, JobSeeker
from accounts.forms                 import *
from social_network.models          import *
from social_network.functions       import *
from jobs.models                    import JobOffer, Skill
from jobs.functions                 import request_pending

from markdown                       import markdown

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
    def getEvent(e):
        if e.type == Event.COMMENT_ON_EMPLOYER:
            return Event_CommentOnEmployer.objects.get(pk=e.pk)
        elif e.type == Event.COMMENT_ON_JOB:
            return Event_CommentOnOpportunity.objects.get(pk=e.pk)
        elif e.type == Event.FRIENDSHIP:
            return Event_FriendShip.objects.get(pk=e.pk)



    if request.userprofile.is_jobseeker():
        js = JobSeeker.objects.get(user = request.user)
        print(js)
        events = Event.objects.all().filter(initial_user = js)
        print(events)
        events = [getEvent(e).summery() for e in events]
        print(events)
        return template(request, 'userpanel/jobseeker/main.html' , {'events' :events})
    elif request.userprofile.is_employer():
        return template(request, 'userpanel/employer/main.html')

@user_required
def userpanel_jobs(request):
    if request.userprofile.is_jobseeker():
        return jobseeker_jobs(request)
    elif request.userprofile.is_employer():
        return employer_jobs(request)

@jobseeker_required
def jobseeker_jobs(request):
    user = request.userprofile
    offers_by_jobseeker = JobOffer.objects.filter(jobSeeker=user, mode=0).order_by('-date')
    offers_by_employer = JobOffer.objects.filter(jobSeeker=user, mode=1).order_by('-date')
    return template(request, 'userpanel/jobseeker/offers.html', {'offers_by_jobseeker' : offers_by_jobseeker, 'offers_by_employer' : offers_by_employer})

@employer_required
def employer_jobs(request):
    user = request.userprofile
    jobs = JobOpportunity.objects.filter(user = user).order_by('-expireDate')
    items = []
    for j in jobs:
        pending = JobOffer.objects.filter(jobOpportunity = j, state = 2).count()
        accepted = JobOffer.objects.filter(jobOpportunity = j, state = 0).count()
        rejected = JobOffer.objects.filter(jobOpportunity = j, state = 1).count()
        items.append( {'job' : j, 'pending':pending, 'accepted' : accepted, 'rejected' : rejected} )
    return template(request, 'userpanel/employer/jobs.html', {'items' : items})

@employer_required
def userpanel_offers(request):
    user = request.userprofile
    offers_by_jobseeker = JobOffer.objects.filter(jobOpportunity__user=user, mode=0).order_by('-date')
    offers_by_employer = JobOffer.objects.filter(jobOpportunity__user=user, mode=1).order_by('-date')
    return template(request, 'userpanel/employer/offers.html', {'offers_by_jobseeker' : offers_by_jobseeker, 'offers_by_employer' : offers_by_employer})


####################################
#######    Info Pages       ########
####################################

@user_required
def userpanel_changeinfo(request):
    if request.userprofile.is_employer():
        return userpanel_changecompanyinfo(request)
    else:
        return userpanel_changejobseekerinfo(request)

@csrf_exempt
def userpanel_info_profile_pages(request):
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

    except Error as e:
        print(e)
        return json_response({'result': 'fail'})


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
        userform = ChangeUserInfoForm(instance = request.userprofile)
        compform = ChangeCompanyInfoForm(instance = request.userprofile)

    context['images'] = list(request.userprofile.images.all())
    context['compform'] = compform
    context['userform'] = userform
    context['site_url'] = settings.SITE_URL

    return render(request, 'userpanel/employer/changecompanyinfo.html', context)


def userpanel_changejobseekerinfo(request):
    pass


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



@jobseeker_required
def userpanel_changejobseekerinfo(request):
    context = {}
    if request.method == 'POST':
        userform = ChangeUserInfoForm(request.POST, request.FILES, instance=request.userprofile)
        jobsform = ChangeJobseekerInfoForm(request.POST, instance=request.userprofile)
        if userform.is_valid() and jobsform.is_valid():
            userform.save()
            jobsform.save()
            context['state'] = 'success'
    else:
        userform = ChangeUserInfoForm(instance = request.userprofile)
        jobsform = ChangeJobseekerInfoForm(instance = request.userprofile)

    context['jobsform'] = jobsform
    context['userform'] = userform
    context['site_url'] = settings.SITE_URL

    return render(request, 'userpanel/jobseeker/changejobseekerinfo.html', context)

@csrf_exempt
def userpanel_changejobseekerinfo_privacy(request):
    is_true = lambda x: x == True or x == 'true' or x == 'True'

    if request.method == 'POST':
        profile = request.userprofile
        if 'access_profile_public' in request.POST:
            profile.access_profile_public = is_true(request.POST['access_profile_public'])
        if 'access_profile_jobseeker' in request.POST:
            profile.access_profile_jobseeker = int(request.POST['access_profile_jobseeker'])
        if 'access_profile_employer' in request.POST:
            profile.access_profile_employer = int(request.POST['access_profile_employer'])
        if 'access_cv_public' in request.POST:
            profile.access_cv_public = is_true(request.POST['access_cv_public'])
        if 'access_cv_jobseeker' in request.POST:
            profile.access_cv_jobseeker = int(request.POST['access_cv_jobseeker'])
        if 'access_cv_employer' in request.POST:
            profile.access_cv_employer = int(request.POST['access_cv_employer'])
        profile.save()

        permissions = {
            'access_profile_public':    profile.access_profile_public,
            'access_profile_jobseeker': profile.access_profile_jobseeker,
            'access_profile_employer':  profile.access_profile_employer,
            'access_cv_public':         profile.access_cv_public,
            'access_cv_jobseeker':      profile.access_cv_jobseeker,
            'access_cv_employer':       profile.access_cv_employer
        }

        print(permissions)

        return json_response({'result': 'success', 'permissions': permissions})
    else:
        return json_response({'result': 'fail', 'error': 'get not supported'})

@csrf_exempt
@jobseeker_required
def userpanel_changejobseekerinfo_skills(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'list possible':
            query = request.POST.get('query', '')
            if query == '':
                skills = Skill.objects.all()
            else:
                skills = Skill.objects.filter(name__contains = query)

            skills = map(lambda x: x.name, skills)
            return json_response({'result': 'success', 'skills': skills})

        elif action == 'list current':
            query = request.POST.get('query', '')
            if query == '':
                skills = request.userprofile.skills.all() 
            else:
                skills = request.userprofile.skills.filter(name__contains = query)
            skills = map(lambda x: x.name, skills)
            return json_response({'result': 'success', 'skills': skills})

        elif action == 'add current':
            skill = request.POST.get('skill', '')
            try:
                request.userprofile.skills.get(name=skill)
            except:
                skill = Skill.objects.get_or_create(name=skill)[0]
                request.userprofile.skills.add(skill)

            skills = request.userprofile.skills.all()
            skills = map(lambda x: x.name, skills)
            return json_response({'result': 'success', 'skills': skills})

        elif action == 'remove current':
            skill = request.POST.get('skill', '')
            try:
                skill = Skill.objects.get(name=skill)
                request.userprofile.skills.remove(skill)
            except:
                pass

            skills = request.userprofile.skills.all()
            skills = map(lambda x: x.name, skills)
            return json_response({'result': 'success', 'skills': skills})
    else:
        return json_response({'result': 'fail', 'error': 'get not supported'})



####################################
#######    Profile Pages    ########
####################################

def comment_to_dict(comment):
    data =  {
        'author': comment.user.full_name,
        'author_url': comment.user.profilePage,
        'date': 'همین الان',
        'content': comment.body
    }

    if comment.user.image:
        data['image'] =  comment.user.image.url
    else:
        data['image'] =  '/static/images/profilepic.png'

    return data

@csrf_exempt
def profile_employer_rate(request, employer_id):
    if request.method == 'POST':
        try:
            employer = Employer.objects.get(pk = employer_id)
        except:
            return json_response({'result': 'fail', 'error': 'employer does not exist'})

        if request.has_profile and request.userprofile.is_jobseeker():
            try:
                rate = int(request.POST['rate'])
            except:
                return json_response({'result': 'fail', 'error': 'no rate given'})

            rate_employer(request.userprofile, employer, rate)
            return json_response({'result': 'success'})
    else:
        return json_response({'result': 'fail', 'error': 'get not supported'})

def profile_employer(request, username):
    employer = Employer.objects.get(user__username = username)
    pages = list(employer.user.pages.all())
    for page in pages:
        page.content = SafeText(markdown(page.content))
    return render(request, 'accounts/employerprofile.html', {'profile': employer, 'pages': pages})

@csrf_exempt
def profile_employer_comments(request, employer_id):
    def list_comments(page, page_size):
        comments = CommentOnEmployer.objects.filter(employer__id = employer_id).order_by('-time')
        p = Paginator(comments, page_size)
        if page > p.num_pages:
            page = p.num_pages
        if page < 0:
            page = 0
        comments = map(comment_to_dict, p.page(page).object_list)
        return json_response({'result': 'success', 'page':page, 'pageCount':p.num_pages , 'comments': comments})

    if request.method == 'POST':
        action = request.POST['action']
        if action == 'list':
            page_size = request.POST.get('page_size', 4)
            page      = int(request.POST.get('page', 1))
            return list_comments(page, page_size)

        elif action == 'add':
            page_size = request.POST.get('page_size', 4)
            body = request.POST['comment']
            employer = Employer.objects.get(pk = employer_id)
            comment  = CommentOnEmployer.objects.create(employer = employer, user = request.userprofile, body = body)
            if request.userprofile.is_jobseeker():
                Event_CommentOnEmployer.objects.create(comment=comment, initial_user=request.userprofile)

            return list_comments(1, page_size)
    else:
        return json_response({'result': 'fail', 'error': 'get not supported'})


def check_profile_access(request, jobseeker):
    if jobseeker.access_profile_public:
        return True
    elif request.userprofile.is_jobseeker():
        if request.userprofile.id == jobseeker.id:
            return True
        elif jobseeker.access_profile_jobseeker == JobSeeker.NO_ACCESS:
            return False
        elif jobseeker.access_profile_jobseeker == JobSeeker.PART_ACCESS:
            return friends(request.userprofile, jobseeker)
        elif jobseeker.access_profile_jobseeker == JobSeeker.ALL_ACCESS:
            return True
    else:
        if jobseeker.access_profile_employer == JobSeeker.NO_ACCESS:
            return False
        elif jobseeker.access_profile_employer == JobSeeker.PART_ACCESS:
            return request_pending(jobseeker, request.userprofile)
        elif jobseeker.access_profile_employer == JobSeeker.ALL_ACCESS:
            return True

def check_cv_access(request, jobseeker):
    if jobseeker.access_cv_public:
        return True
    elif request.userprofile.is_jobseeker():
        if request.userprofile.id == jobseeker.id:
            return True
        elif jobseeker.access_cv_jobseeker == JobSeeker.NO_ACCESS:
            return False
        elif jobseeker.access_cv_jobseeker == JobSeeker.PART_ACCESS:
            return friends(request.userprofile, jobseeker)
        elif jobseeker.access_cv_jobseeker == JobSeeker.ALL_ACCESS:
            return True
    else:
        if jobseeker.access_cv_employer == JobSeeker.NO_ACCESS:
            return False
        elif jobseeker.access_cv_employer == JobSeeker.PART_ACCESS:
            return request_pending(jobseeker, request.userprofile)
        elif jobseeker.access_cv_employer == JobSeeker.ALL_ACCESS:
            return True    

def profile_jobseeker(request, username):
    context = {}

    jobseeker = JobSeeker.objects.get(user__username = username)
    context['profile'] = jobseeker

    if not check_profile_access(request, jobseeker):
        raise PermissionDenied

    # Friendship
    if not request.has_profile:
        context['is_friend'] = False
    elif request.userprofile.is_jobseeker():
        context['is_friend'] = friends(request.userprofile, jobseeker)

    # CV Access:
    context['cv_access'] = check_cv_access(request, jobseeker)

    skills = jobseeker.skills.all()
    skills = map(lambda x: x.name, skills)
    context['skills'] = skills

    pages = list(jobseeker.user.pages.all())
    for page in pages:
        page.content = SafeText(markdown(page.content))
    context['pages'] = pages

    return render(request, 'accounts/jobseekerprofile.html', context)

def profile_jobseeker_getcv(request, jobseeker_id):
    try:
        jobseeker = JobSeeker.objects.get(pk=jobseeker_id)
    except:
        raise Http404

    if check_cv_access(request, jobseeker):
        print(jobseeker.cv.url)
        # Dirty Fix
        return serve(request, document_root=settings.MEDIA_ROOT, path=jobseeker.cv.url[7:])
    else:
        raise PermissionDenied


