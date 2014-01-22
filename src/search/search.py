from jobs.models import JobOpportunity

def opportunity(query, skills):
	return JobOpportunity.objects.all()

def skill():
	pass

def user():
	pass