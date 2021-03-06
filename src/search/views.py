from accounts.models import JobSeeker, Employer
from jobs.models import JobOpportunity, JobOffer
from social_network.models import RateForOpportunity, RateForEmployer
import json
import search
from django.shortcuts            import render
from django.http                 import HttpResponse
import math
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

@csrf_exempt
def opSearch(request):
    request.session['lastSearch'] = 'job'
    pageSize = 4
    curPage = 1
    user = request.user
    if request.method == "GET":
        param = request.GET
    elif request.method == 'POST':
        param = request.POST
    query = param.get('q') or ""
    print('query', query)
    skills = []
    try:
        skills = json.loads(param.get('sk'))
    except Exception as ex:
        print('ok')
        # print(type(ex).__name__)
        # print(ex.args)    

    try:
        curPage = int(param.get('page'))
    except Exception as ex:
        print type(ex).__name__
        print ex.args
        curPage = 1

    if curPage < 1:
        curPage = 1

    print("skills", skills)
    print('curPage', curPage)

    if not 'ajax' in param and user.is_authenticated() and len(skills) == 0:
        try:
            skillOb = JobSeeker.objects.all().get(user__username = user.username).skills.all()
            for sob in skillOb:
                skills.append(sob.name)
        except Exception as ex:
            # template = "An exception of type {0} occured. Arguments:\n{1!r}"
            # message = template.format(type(ex).__name__, ex.args)
            # print message
            skills = []

    search_result = search.opportunity(query, skills)
    start = (curPage - 1) * pageSize
    next = True
    pre = False
    count = len(search_result)
    
    if count < start + 1:
        search_result = search_result[0:pageSize]
    else:
        search_result = search_result[start:start+pageSize]
        if curPage > 1:
            pre = True
        if count <= curPage * pageSize:
            next = False


    pageNum = int(math.ceil((count + 0.0) / pageSize))
    pages = []
    if  pageNum <= 5:
        pages = [str(i + 1) for i in range(pageNum)]
    else:
        if curPage % 3 == 0:
            base = curPage - 2
        else:
            base = (curPage / 3) * 3 + 1
        if pageNum - curPage < 3:
            pages = ['1', '...', str(pageNum - 2), str(pageNum - 1), str(pageNum)]
        else:
            pages = [str(base), str(base + 1), str(base + 2), '...', str(pageNum)]

    appliedFor = JobOpportunity.objects.filter(offers__jobSeeker = request.userprofile).exclude(offers__state=2)
    pending = JobOpportunity.objects.filter(offers__jobSeeker = request.userprofile, offers__state=2)

    context = {'query':query, 'skills' : skills, 'skill_result' : [], 'search_result' : search_result, 'pages':pages, 'next':next, 'pre' : pre, 'curPage' : str(curPage), 'pending' : pending, 'appliedFor' : appliedFor}
    return render(request, 'search/opSearch.html', context)


def skillSearch(request):
    param = request.GET
    skills = []
    if 'q' in param:
        query = param.get('q')
        if len(query) > 0:
            skills = search.skill(query)
        else:
            skills = []
    # print(skills)
    context = {'skills' : [], 'skill_result' : skills, 'search_result' : []}
    return render(request, 'search/opSearch.html', context)    


@login_required
def updateRate(request):
    param = request.GET
    response={}
    if 'rate' in param:
        if 'op' in param:

            try:
                op = JobOpportunity.objects.get(id = int(param.get('op')))
                ratings = RateForOpportunity.objects.filter(user__user__username = request.user.username).filter(opportunity__id = op.id)
                if len(ratings) == 0:
                    seeker = JobSeeker.objects.get(user__username = request.user.username)
                    r = RateForOpportunity(user = seeker, opportunity = op, rate = int(param.get('rate')))
                    r.save()
                else:
                    ratings[0].rate = int(param.get('rate'))
                    ratings[0].save()
            except Exception as ex:
                print(type(ex).__name__)
                print(ex.args)
                response['result'] = 0
                print('here1')
                return HttpResponse(json.dumps(response), content_type="application/json")

            response['result'] = 1
            response['rate'] = op.rate
            # print('here2')
            return HttpResponse(json.dumps(response), content_type="application/json")

        elif 'emp' in param:
            try:
                emp = Employer.objects.get(id = int(param.get('emp')))
                ratings = RateForEmployer.objects.filter(user__user__username = request.user.username).filter(employer__id = emp.id)
                if len(ratings) == 0:
                    seeker = JobSeeker.objects.get(user__username = request.user.username)
                    r = RateForEmployer(user = seeker, employer = emp, rate = int(param.get('rate')))
                    r.save()

                else:
                    ratings[0].rate = int(param.get('rate'))
                    ratings[0].save()
            except Exception as ex:
                print(type(ex).__name__)
                print(ex.args)
                response['result'] = 0
                print('here1')
                return HttpResponse(json.dumps(response), content_type="application/json")

            response['result'] = 1
            response['rate'] = emp.rate
            # print('here2')
            return HttpResponse(json.dumps(response), content_type="application/json")

    response['result'] = 0
    # print('here3')
    return HttpResponse(json.dumps(response), content_type="application/json")

@csrf_exempt
@login_required
def userSearch(request):
    request.session['lastSearch'] = 'user'
    pageSize = 4
    curPage = 1
    if request.method == "GET":
        param = request.GET
    elif request.method == "POST":
        param = request.POST
    query = param.get('q') or ""
    print('query', query)
    skills = []
    try:
        skills = json.loads(param.get('sk'))
    except Exception as ex:
        print('ok')
        # print(type(ex).__name__)
        # print(ex.args)    

    try:
        curPage = int(param.get('page'))
    except Exception as ex:
        print type(ex).__name__
        print ex.args
        curPage = 1

    if curPage < 1:
        curPage = 1

    print("skills", skills)
    print('curPage', curPage)

    
    search_result = search.user(query, skills)
    start = (curPage - 1) * pageSize
    next = True
    pre = False
    count = len(search_result)

    if count < start + 1:
        search_result = search_result[0:pageSize]
    else:
        search_result = search_result[start:start+pageSize]
        if curPage > 1:
            pre = True
        if count <= curPage * pageSize:
            next = False


    pageNum = int(math.ceil((count + 0.0) / pageSize))
    pages = []
    if  pageNum <= 5:
        pages = [str(i + 1) for i in range(pageNum)]
    else:
        if curPage % 3 == 0:
            base = curPage - 2
        else:
            base = (curPage / 3) * 3 + 1
        if pageNum - curPage < 3:
            pages = ['1', '...', str(pageNum - 2), str(pageNum - 1), str(pageNum)]
        else:
            pages = [str(base), str(base + 1), str(base + 2), '...', str(pageNum)]

    context = {'query': query, 'skills' : skills, 'skill_result' : [], 'search_result' : search_result, 'pages':pages, 'next':next, 'pre' : pre, 'curPage' : str(curPage)} 
    return render(request, 'search/userSearch.html', context)
