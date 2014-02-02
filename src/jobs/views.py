#coding=utf-8

from datetime                       import datetime
from django.core.serializers        import json
from django.http.response           import HttpResponse
from django.views.decorators.csrf   import csrf_exempt
from django.core.paginator          import Paginator
from django.core.exceptions         import PermissionDenied

from accounts.decorators            import *
from accounts.views                 import userpanel_jobs
from jobs.forms                     import JobForm
from jobs.models                    import *
from social_network.models          import *
from social_network.functions       import *
from utils.functions                import json_response, template

@jobseeker_required
def applyJob(request, jobid):
    print 'hey'
    print jobid
    job = JobOpportunity.objects.get(id = jobid)
    user = request.userprofile
    response = {}
    if not JobOffer.objects.filter(jobSeeker = user, jobOpportunity = job).exists():
        JobOffer.objects.create(jobSeeker = user, jobOpportunity = job, offerDate = datetime.now())
        response['done'] = True
    else:
        response['done'] = False
    return json_response(response)

@jobseeker_required
def refuseJob(request, jobid):
    job = JobOpportunity.objects.get(id = jobid)
    user = request.userprofile
    response = {}
    if JobOffer.objects.filter(jobSeeker = user, jobOpportunity = job).exists():
        JobOffer.objects.filter(jobSeeker = user, jobOpportunity = job).delete()
        response['done'] = True
    else:
        response['done'] = False
    return json_response(response)

@employer_required
def acceptOffer(request, offerid):
    offer = JobOffer.objects.get(id = offerid)
    offer.state = 0
    offer.offerDate = datetime.now()
    offer.save()
    return json_response({})

@employer_required
def rejectOffer(request, offerid):
    offer = JobOffer.objects.get(id = offerid)
    offer.state = 1
    offer.save()
    return json_response({})

@employer_required
def deleteJob(request, jobid):
    JobOpportunity.objects.get(id = jobid).delete()
    return json_response({})

@employer_required
def editJob(request, jobid):
    job = JobOpportunity.objects.get(id = jobid)
    show_extra = False
    if request.method == "POST":
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            show_extra = True
            return userpanel_jobs(request)
    else:
        show_extra = True
        form = JobForm(instance = job)
    return template(request, 'userpanel/employer/editJob.html', {'form' : form, 'show_extra': show_extra})

@employer_required
def newJob(request):
    show_extra = False
    if request.method == "POST":
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(False)
            job.user = request.userprofile
            job.save()
            show_extra = True
            return template(request, 'userpanel/employer/editJob.html', {'form' : form, 'show_extra': True, 'scroll_to_extra': True})
    else:
        form = JobForm()
    return template(request, 'userpanel/employer/editJob.html', {'form' : form, 'show_extra':show_extra})

def jobPage(request, jobid):
    job = JobOpportunity.objects.get(id = jobid)
    skills = map(lambda x: x.name, job.opSkills.all())
    pages = list(job.pages.all())
    return template(request, 'jobs/jobsPage.html', {'job' : job, 'skills':skills, 'pages':pages})


@csrf_exempt
def job_opportunity_pages(request, opportunity_id):
    action = request.POST.get('action', '')
    try:
        opportunity = JobOpportunity.objects.get(pk = opportunity_id)
        if action == 'save':
            page_id = request.POST['page_id']
            content = request.POST['content']
            page = JobOpportunityPage.objects.get(pk = page_id)
            if page.opportunity.id != opportunity_id:
                raise PermissionDenied
            page.content = content
            page.save()
            return json_response({'result': 'success'})

        elif action == 'remove':
            page_id = request.POST['page_id']
            page = JobOpportunityPage.objects.get(pk = page_id)
            if page.opportunity.id != opportunity_id:
                raise PermissionDenied
            page.delete()
            return json_response({'result': 'success'})

        elif action == 'add':
            title = request.POST['title']
            page = JobOpportunityPage.objects.create(opportunity=opportunity, title=title)
            page = {'page_id': page.id, 'title':page.title, 'content': page.content}
            return json_response({'result': 'success', 'page': page})

        elif action == 'list':
            pages = JobOpportunityPage.objects.filter(opportunity=opportunity)
            pages = map(lambda x: {'page_id': x.id, 'title':x.title, 'content': x.content}, pages)
            return json_response({'result': 'success', 'pages': pages})

    except Exception as e:
        raise e
        return json_response({'result': 'fail'})

@csrf_exempt
def job_opportunity_skills(request, opportunity_id):
    if request.method == 'POST':
        action = request.POST.get('action')
        try:
            opportunity = JobOpportunity.objects.get(pk = opportunity_id)
        except:
            return json_response({'result': 'fail', 'error': 'job opportunity not found'})

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
                skills = opportunity.opSkills.all() 
            else:
                skills = opportunity.opSkills.filter(name__contains = query)
            skills = map(lambda x: x.name, skills)
            return json_response({'result': 'success', 'skills': skills})

        elif action == 'add current':
            skill = request.POST.get('skill', '')
            try:
                opportunity.opSkills.get(name=skill)
            except:
                skill = Skill.objects.get_or_create(name=skill)[0]
                opportunity.opSkills.add(skill)

            skills = opportunity.opSkills.all()
            skills = map(lambda x: x.name, skills)
            return json_response({'result': 'success', 'skills': skills})

        elif action == 'remove current':
            skill = request.POST.get('skill', '')
            try:
                skill = Skill.objects.get(name=skill)
                opportunity.opSkills.remove(skill)
            except:
                pass

            skills = opportunity.opSkills.all()
            skills = map(lambda x: x.name, skills)
            return json_response({'result': 'success', 'skills': skills})
    else:
        return json_response({'result': 'fail', 'error': 'get not supported'})

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
def job_comment(request, job_id):
    try:
        job = JobOpportunity.objects.get(pk = job_id)
    except:
        return json_response({'result':'fail', 'error':'job not found'})

    def list_comments(page, page_size):
        comments = CommentOnOpportunity.objects.filter(opportunity = job).order_by('-time')
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
            comment  = CommentOnOpportunity.objects.create(opportunity = job, user = request.userprofile, body = body)
            if request.userprofile.is_jobseeker():
                Event_CommentOnOpportunity.objects.create(comment=comment, initial_user=request.userprofile)

            return list_comments(1, page_size)
    else:
        return json_response({'result': 'fail', 'error': 'get not supported'})

@csrf_exempt
def job_rate(request, job_id):
    if request.method == 'POST':
        try:
            job = JobOpportunity.objects.get(pk = job_id)
        except:
            return json_response({'result': 'fail', 'error': 'job does not exist'})

        if request.has_profile and request.userprofile.is_jobseeker():
            try:
                rate = int(request.POST['rate'])
            except:
                return json_response({'result': 'fail', 'error': 'no rate given'})

            rate_opportunity(request.userprofile, job, rate)
            return json_response({'result': 'success'})
    else:
        return json_response({'result': 'fail', 'error': 'get not supported'})