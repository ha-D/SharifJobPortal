from django.contrib.auth.views 		import login, logout
from django.shortcuts            	import render, render_to_response
from django.template             	import RequestContext
from django.template.loader     	import render_to_string
from django.http                 	import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models 	import User
from social_network.models          import *

from jobs.models import JobOffer
from utils.functions		 		import template, json_response, ajax_template
from accounts.decorators 			import user_required, jobseeker_required, employer_required
from accounts.forms                	import *
from django.conf 					import settings


JOBSEEKER_SESSION = 'register_jobseeker'
EMPLOYER_SESSION = 'register_employer'

def register_jobseeker_skills(request, session_name):
	if request.method == 'POST':
		return json_response({'result': 1}), 1

	return json_response({
	    'result': 1,
	    'data': render_to_string('accounts/register/jobseeker/skills.html', RequestContext(request))
	}), None


def register_jobseeker_finalize(request, session_name):
    session_steps = request.session[session_name]['steps']

    user = session_steps['user_info']
    jobseeker = session_steps['personal_info']
    jobseeker_work = session_steps['work_info']

    user.save()

    jobseeker.user = user
    jobseeker.job_status = jobseeker_work.job_status
    jobseeker.cv = jobseeker_work.cv
    jobseeker.save()

    del request.session[session_name]

    return json_response({
    	'result': 1,
    	'data': render_to_string('accounts/register/jobseeker/final.html', RequestContext(request))
    }), None

def register_employer_finalize(request, session_name):
    session_steps = request.session[session_name]['steps']

    user = session_steps['user_info']
    employer = session_steps['company_info']

    user.save()

    employer.user = user
    employer.save()
    
    del request.session[session_name]

    return json_response({
    	'result': 1,
    	'data': render_to_string('accounts/register/employer/final.html', RequestContext(request))
    }), None	

def register_form(request, session_name, template, step, register_form):
	if request.method == 'POST':
		form = register_form(request.POST)
		if form.is_valid():
			request.session[session_name]['post'][step] = request.POST
			obj = form.save()
			return json_response({'result': 1}), obj
		else:
			result = 0
	else:
		post = request.session[session_name]['post'].get(step)
		form =  register_form() if post == None else register_form(post)
		result = 1

	return json_response({
		'result': result,
		'data': render_to_string('accounts/register/' + template, RequestContext(request, {'form': form}))
	}), None

def register(request, action, steps, step_views, session_name, base_template):
	if action == 'ajax':
		step = request.GET.get('step')
		step = steps.index(step) if step in steps else None

		state = request.session.get(session_name)
		if step == None or state == None:
			step = 0
			state = {
				'current_step': 0,
				'steps': {},
				'post': {}
			}
			request.session[session_name] = state
			request.session.save()


		# No skipping steps  faulty, doesn't work for skills
		# if state['current_step'] < step:
		# 	print("No skipping " + str(state['current_step']) + " < " +  str(step))
		# 	step = state['current_step']

		response, result =  step_views[steps[step]](request, session_name)

		if result != None:
			state['steps'][steps[step]] = result
			if state['current_step'] == step:
				state['current_step'] += 1
		
		request.session.save()

		return response

	elif action == 'steps':
		return json_response({'steps': steps})

	elif action == 'clear':
		if session_name in request.session:
			del request.session[session_name]
		return HttpResponse("Cleared")

	else:
		return render_to_response('accounts/register/' + base_template)



def _lambda(template, step, form):
    return lambda req, session: register_form(request=req, session_name=session, template=template, step=step,
        register_form=form)


def register_jobseeker(request, action):
    steps = ['user_info', 'personal_info', 'work_info', 'skills', 'confirm', 'finalize']
    step_views = {
        'user_info':     _lambda('user_info.html', 'user_info', RegisterUserForm),
        'personal_info': _lambda('jobseeker/personal_info.html', 'personal_info', JobSeekerRegisterProfileForm),
        'work_info':     _lambda('jobseeker/work_info.html', 'work_info', JobSeekerRegisterWorkForm),
        'skills':         register_jobseeker_skills,
        'confirm':       _lambda('confirm.html', 'confirm', RegisterFinalForm),
        'finalize':       register_jobseeker_finalize
    }

    return register(request, action, steps, step_views, JOBSEEKER_SESSION, 'jobseeker.html')


def register_employer(request, action):
    steps = ['user_info', 'company_info', 'confirm', 'finalize']
    step_views = {
        'user_info':    _lambda('user_info.html', 'user_info', RegisterUserForm),
        'company_info': _lambda('employer/company_info.html', 'company_info', EmployerRegisterProfileForm),
        'confirm':      _lambda('confirm.html', 'confirm', RegisterFinalForm),
        'finalize':      register_employer_finalize
    }

    return register(request, action, steps, step_views, EMPLOYER_SESSION, 'employer.html')


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
def userpanel(request):
    if request.userprofile.is_jobseeker():
        return template(request, 'userpanel/jobseeker.html')
    elif request.userprofile.is_employer():
        return template(request, 'userpanel/employer.html')

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
        events = Event.objects.all()
        events = [ getEvent(e).summery() for e in events]
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