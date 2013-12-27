from django.shortcuts			import render, render_to_response
from django.template 			import RequestContext
from django.template.loader 	import render_to_string
from django.http 				import HttpResponse
from django.contrib.auth.models import User
from accounts.forms				import JobSeekerRegisterUserForm, JobSeekerRegisterProfileForm, JobSeekerRegisterWorkForm, JobSeekerRegisterFinalForm

import json

def json_response(response):
	return HttpResponse(json.dumps(response))

def register_jobseeker_form(request, step, register_form):
	if request.method == 'POST':
		request.session['register_state']['post'][step] = request.POST
		form = register_form(request.POST)
		if form.is_valid():
			obj = form.save(commit = False)
			return json_response({'result': 1}), obj
		else:
			result = 0
	else:
		post = request.session['register_state']['post'].get(step)
		form =  register_form() if post == None else register_form(post)
		result = 1

	return json_response({
		'result': result,
		'data': render_to_string('register/%s.html' % step, RequestContext(request, {'form': form}))
	}), None


def register_jobseeker_skills(request):
	if request.method == 'POST':
		return json_response({'result': 1}), None

	return json_response({
		'result': 1,
		'data': render_to_string('register/skills.html', RequestContext(request))
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
		'user_info': 	 lambda req: register_jobseeker_form(req, 'user_info', 	  JobSeekerRegisterUserForm),
		'personal_info': lambda req: register_jobseeker_form(req, 'personal_info', JobSeekerRegisterProfileForm),
		'work_info': 	 lambda req: register_jobseeker_form(req, 'work_info', 	  JobSeekerRegisterWorkForm),
		'skills': 		 register_jobseeker_skills,
		'confirm': 		 lambda req: register_jobseeker_form(req, 'confirm', 	  JobSeekerRegisterFinalForm),
		'finalize': 	 register_jobseeker_finalize
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
				'steps': {},
				'post': {}
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