from django.shortcuts               import render, render_to_response
from django.template                import RequestContext
from django.template.loader         import render_to_string
from django.http                    import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models     import User
from django.conf                    import settings
from django.views.decorators.csrf   import csrf_exempt

from shutil                         import copy
from os                             import remove

from utils.functions                import template, json_response, ajax_template
from accounts.decorators            import user_required
from accounts.forms                 import *
from jobs.models                    import Skill

JOBSEEKER_SESSION = 'register_jobseeker'
EMPLOYER_SESSION = 'register_employer'

@csrf_exempt
def register_jobseeker_skills_handle(request):
    if request.method == 'POST':
        steps = request.session[JOBSEEKER_SESSION].get('steps')
        if steps == None:
            return json_response({'result':'fail', 'error':'no state set'})

        current_skills = steps.get('skills')

        if current_skills == None or type(current_skills) != set:
            current_skills = set()
            steps['skills'] = current_skills

        try:
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
                skills = filter(lambda x: query == '' or query in x, current_skills)
                return json_response({'result': 'success', 'skills': skills})

            elif action == 'add current':
                skill = request.POST.get('skill', '')
                current_skills.add(skill)
                return json_response({'result': 'success', 'skills': list(current_skills)})

            elif action == 'remove current':
                skill = request.POST.get('skill', '')
                try:
                    current_skills.remove(skill)
                except:
                    pass
                return json_response({'result': 'success', 'skills': list(current_skills)})
        finally:
            request.session.save()
    else:
        return json_response({'result': 'fail', 'error': 'get not supported'})

def register_jobseeker_skills(request, session_name):
    if request.method == 'POST':
        return json_response({'result': 1}), True, None

    return json_response({
        'result': 1,
        'data': render_to_string('accounts/register/jobseeker/skills.html', RequestContext(request))
    }), False, None

from django.core.files import File
def register_jobseeker_finalize(request, session_name):
    session_steps = request.session[session_name]['steps']

    user = session_steps['user_info']
    jobseeker = session_steps['personal_info']
    jobseeker_work = session_steps['work_info']


    user.save()

    jobseeker.user = user
    jobseeker.job_status = jobseeker_work.job_status

    dest_file = 'cv/cv_%s.pdf' % user.username
    src_file = 'cv/%s' % jobseeker_work.cv_filename
    f = open(settings.MEDIA_ROOT + src_file)
    jobseeker.cv.save(dest_file, File(f))
    f.close()
    remove(settings.MEDIA_ROOT + src_file)

    jobseeker.save()

    skills = list(session_steps.get('skills', []))
    for skill in skills:
        jobseeker.skills.add(Skill.objects.get_or_create(name=skill)[0])


    del request.session[session_name]

    return json_response({
        'result': 1,
        'data': render_to_string('accounts/register/final.html', RequestContext(request))
    }), False, None

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
        'data': render_to_string('accounts/register/final.html', RequestContext(request))
    }), False, None    

def register_form(request, session_name, template, step, register_form):
    if request.method == 'POST':
        form = register_form(request.POST, request.FILES)
        if form.is_valid():
            request.session[session_name]['post'][step] = request.POST
            obj = form.save(commit=False)
            return json_response({'result': 1}), True, obj
        else:
            result = 0
    else:
        post = request.session[session_name]['post'].get(step)
        form =  register_form() if post == None else register_form(post)
        result = 1

    return json_response({
        'result': result,
        'data': render_to_string('accounts/register/' + template, RequestContext(request, {'form': form}))
    }), False, None

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
        if state['current_step'] < step:
          # print("No skipping " + str(state['current_step']) + " < " +  str(step))
          step = state['current_step']

        response, next, result =  step_views[steps[step]](request, session_name)

        if next:
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