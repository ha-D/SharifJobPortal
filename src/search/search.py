 # -*- coding: utf-8 -*-
from jobs.models import JobOpportunity
from jobs.models import Skill
from django.db.models import Q
import datetime

def opportunity(query, skills):
	words = [s.strip() for s in query.split(' ')]
	biwordsOps = None
	normalOps = JobOpportunity.objects.filter(getFinalQuery(words)).filter(expireDate__gt = datetime.date.today())
	if len(words) > 1:
		words2 = words[1:] + [words[0]]
		biwords = [ s + " " + k for s,k in zip(words, words2)]
		# user.username user.companyName, name
		biwordsOps = JobOpportunity.objects.filter(getFinalQuery(biwords)).filter(expireDate__gt = datetime.date.today())
	
	rank(normalOps, biwordsOps, skills, words)
	return JobOpportunity.objects.all()

def getFinalQuery(words):
	userNameQueryList = [Q(user__user__username__contains = w) for w in words]
	companyNameQueryList = [Q(user__companyName__contains = w) for w in words]
	nameQueryList = [Q(name__contains = w) for w in words]
	finalQuery = userNameQueryList[0]
	if len(finalQuery) > 1:
		for q in finalQuery[1:]:
			finalQuery = finalQuery | q
	for q in companyNameQueryList:
		finalQuery = finalQuery | q
	for q in nameQueryList:
		finalQuery = finalQuery | q
	return finalQuery

def rank(normalOps, biwordsOps, skills, words):
	refineNormal = []
	if biwordsOps and normalOps:
		refineNormal = [n for n in normalOps if n not in biwordsOps]
		allOps = biwordsOps + refineNormal
	elif biwordsOps:
		allOps = biwordsOps
	else:
		allOps = normalOps

	print('allops', allOps)
	#sex
	sex = None
	if u'مرد' in words and not u'زن' in words:
		sex = 0
	elif u'زن' in words and not u'مرد' in words:
		sex = 1
	if not sex is None:
		sexFilter = allOps.filter(sex = sex)
	else:
		sexFilter = allOps
	print('filter1', sexFilter)

	skillMatch = {}
	for op in allOps:
		skillName = [s.name for s in op.opSkills.all()]
		intersect = filter(lambda x : x in skills, skillName)
		skillMatch[op.id] = len(intersect)

	print('skill', skillMatch)

	#salary

def skill(query):
	return Skill.objects.filter(name__startswith = query)

def user():
	pass