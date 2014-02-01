# Create your views here.
from datetime import datetime
from django.core.serializers import json
from django.http.response import HttpResponse
from accounts.decorators import employer_required
from accounts.views import userpanel_jobs
from jobs.forms import JobForm
from jobs.models import JobOpportunity, JobOffer
from utils.functions1 import json_response, template

@employer_required
def applyJob(request, jobid):
    job = JobOpportunity.objects.get(id = jobid)
    user = request.userprofile
    response = {}
    if not JobOffer.objects.filter(jobSeeker = user, jobOpportunity = job).exists():
        JobOffer.objects.create(jobSeeker = user, jobOpportunity = job, offerDate = datetime.now())
        response['done'] = True
    else:
        response['done'] = False
    return json_response(response)

@employer_required
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
    if request.method == "POST":
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return userpanel_jobs(request)
    else:
        form = JobForm(instance = job)
    return template(request, 'userpanel/employer/editJob.html', {'form' : form})

@employer_required
def newJob(request):
    if request.method == "POST":
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(False)
            job.user = request.userprofile
            job.save()
            return userpanel_jobs(request)
    else:
        form = JobForm()
    return template(request, 'userpanel/employer/editJob.html', {'form' : form})

@employer_required
def jobPage(request, jobid):
    job = JobOpportunity.objects.get(id = jobid)
    return template(request, 'jobs/jobsPage.html', {'job' : job})