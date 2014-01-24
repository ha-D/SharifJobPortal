# Create your views here.
from datetime import datetime
from django.core.serializers import json
from django.http.response import HttpResponse
from jobs.models import JobOpportunity, JobOffer
from utils.functions import json_response

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

def acceptOffer(request, offerid):
    offer = JobOffer.objects.get(id = offerid)
    offer.state = 0
    offer.offerDate = datetime.now()
    offer.save()
    return json_response({})

def rejectOffer(request, offerid):
    offer = JobOffer.objects.get(id = offerid)
    offer.state = 1
    offer.save()
    return json_response({})
