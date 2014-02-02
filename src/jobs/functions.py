from accounts.models import *


def request_pending(jobseeker, opportunity):
	return JobOffer.objects.filter(jobSeeker=jobseeker, jobOpportunity=opportunity, state=2).exists()