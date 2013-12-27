from django.shortcuts			import render, render_to_response
from django.template 			import RequestContext
from django.template.loader 	import render_to_string
from django.http 				import HttpResponse
from django.contrib.auth.models import User
from accounts.forms				import JobSeekerRegisterUserForm, JobSeekerRegisterProfileForm, JobSeekerRegisterWorkForm, JobSeekerRegisterFinalForm

import json

def json_response(response):
	return HttpResponse(json.dumps(response))
	
def register_jobseeker_userinfo(request):
	if request.method == 'POST':
		form = JobSeekerRegisterUserForm(request.POST)
		if form.is_valid():
			user = form.save(commit = False)
			return json_response({'result': 1}), user
		else:
			result = 0
	else:
		result = 1

	return json_response({
		'result': result,
		'data': render_to_string('register/user_info.html', RequestContext(request, {'form': form}))
	}), None

def register_jobseeker_personal(request):
	if request.method == 'POST':
		form = JobSeekerRegisterProfileForm(request.POST)
		if form.is_valid():
			jobseeker = form.save(commit = False)
			return json_response({'result': 1}), jobseeker
		else:
			result = 0
	else:
		form = JobSeekerRegisterProfileForm()
		result = 1

	return json_response({
		'result': result,
		'data': render_to_string('register/personal_info.html', RequestContext(request, {'form': form}))
	}), None

def register_jobseeker_work(request):
	if request.method == 'POST':
		form = JobSeekerRegisterWorkForm(request.POST)
		if form.is_valid():
			jobseeker = form.save(commit = False)
			return json_response({'result': 1}), jobseeker
		else:
			result = 0
	else:
		form = JobSeekerRegisterWorkForm()
		result = 1

	return json_response({
		'result': result,
		'data': render_to_string('register/work_info.html', RequestContext(request, {'form': form}))
	}), None

def register_jobseeker_skills(request):
	if request.method == 'POST':
		return json_response({'result': 1}), None

	return json_response({
		'result': 1,
		'data': render_to_string('register/skills.html', RequestContext(request))
	}), None

def register_jobseeker_confirm(request):
	if request.method == 'POST':
		form = JobSeekerRegisterFinalForm(request.POST)
		if form.is_valid():
			return json_response({'result': 1}), None
		else:
			result = 0
	else:
		form = JobSeekerRegisterFinalForm()
		result = 1
	
	return json_response({
		'result': result,
		'data': render_to_string('register/confirm.html', RequestContext(request, {'form': form}))
	}), None	

def register_jobseeker_finalize(request):
	session_steps = request.session['register_state']['steps']

	user = session_steps['user_info']
	jobseeker = session_steps['personal_info']
	jobseeker_work = session_steps['work_info']

	user.save()
	
	jobseeker.user = user
	jobseeker.job_status = jobseeker_work.job_status
	jobseeker.cv = jobseeker_work.cv
	jobseeker.save()

	return json_response({
		'result': 1,
		'data': render_to_string('register/final.html', RequestContext(request))
	}), None


def register_jobseeker(request, action):
	steps = ['user_info', 'personal_info', 'work_info', 'skills', 'confirm', 'finalize']
	step_views = {
		'user_info': register_jobseeker_userinfo,
		'personal_info': register_jobseeker_personal,
		'work_info': register_jobseeker_work,
		'skills': register_jobseeker_skills,
		'confirm': register_jobseeker_confirm,
		'finalize': register_jobseeker_finalize
	}

	if action == 'ajax':
		step = request.GET.get('step')
		step = steps.index(step) if step in steps else None

		state = request.session.get('register_state')
		print("State:  " + str(state))
		if step == None or state == None:
			print("No state found making one")
			step = 0
			state = {
				'current_step': 0,
				'steps': {}
			}
			request.session['register_state'] = state
			request.session.save()


		# No skipping steps
		# if state['current_step'] < step:
		# 	print("No skipping " + str(state['current_step']) + " < " +  str(step))
		# 	step = state['current_step']

		response, result =  step_views[steps[step]](request)

		if result != None:
			state['steps'][steps[step]] = result
			if state['current_step'] == step:
				state['current_step'] += 1
			request.session.save()

		return response

	elif action == 'steps':
		return json_response({'steps': steps})
	else:
		return render_to_response('register.html')