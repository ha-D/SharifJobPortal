from jobs.models import JobOpportunity
from jobs.models import Skill

def opportunity(query, skills):
	return JobOpportunity.objects.all()

def skill(query):
	return Skill.objects.filter(name__startswith = query)

def user():
	pass