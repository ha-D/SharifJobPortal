# Create your views here.
from datetime import datetime
from django.core.serializers import json
from django.http.response import HttpResponse
from jobs.models import JobOpportunity, JobOffer
from utils.functions import json_response

def applyJob(request, jobid):
    job = JobOpportunity.objects.get(id = jobid)
    user = request.userprofile
    if not JobOffer.objects.filter(jobSeeker = user, jobOpportunity = job).exists():
        JobOffer.objects.create(jobSeeker = user, jobOpportunity = job, offerDate = datetime.now())
    return json_response({})

def refuseJob(request, jobid):
    job = JobOpportunity.objects.get(id = jobid)
    user = request.userprofile
    res = {}
    if JobOffer.objects.filter(jobSeeker = user, jobOpportunity = job).exists():
        JobOffer.objects.filter(jobSeeker = user, jobOpportunity = job).delete()
    return json_response({})