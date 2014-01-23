 # -*- coding: utf-8 -*-
from jobs.models import JobOpportunity
from jobs.models import Skill
from django.db.models import Q
import datetime

def opportunity(query, skills):
	if len(query) == 0:
		return JobOpportunity.objects.all().filter(expireDate__gt = datetime.date.today())
	words = [s.strip() for s in query.split(' ')]
	biwordsOps = None
	normalOps = JobOpportunity.objects.filter(getFinalQuery(words)).filter(expireDate__gt = datetime.date.today())
	if len(words) > 1:
		words2 = words[1:] + [words[0]]
		biwords = [ s + " " + k for s,k in zip(words, words2)]
		# user.username user.companyName, name
		finalBiwordQuery = getFinalQuery(biwords)
		biwordsOps = JobOpportunity.objects.filter(finalBiwordQuery).filter(expireDate__gt = datetime.date.today())
		normalOps = normalOps.exclude(finalBiwordQuery)
	res = []
	ranks = rank(normalOps, biwordsOps, skills, words)
	for r in ranks:
		res.append(JobOpportunity.objects.get(id = r))
	return res

	

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
	if biwordsOps and normalOps:
		allOps = biwordsOps | normalOps
	elif biwordsOps:
		allOps = biwordsOps
	else:
		allOps = normalOps

	if biwordsOps:	
		biwordsOps = [op.id for op in biwordsOps]
	else:
		biwordsOps = []

	print('allops', allOps)
	#sex
	sex = None
	if u'مرد' in words and not u'زن' in words:
		sex = 0
	elif u'زن' in words and not u'مرد' in words:
		sex = 1
	if not sex is None:
		sexFilter = allOps.filter(sex = sex)
		opSexFilter = allOps.filter(sex = 1 - sex)
	else:
		sexFilter = allOps
		opSexFilter = []
	print('filter1', sexFilter)
	sexFilter = [op.id for op in sexFilter]
	opSexFilter = [op.id for op in opSexFilter]

	skillMatch = {}
	for op in allOps:
		skillName = [s.name for s in op.opSkills.all()]
		intersect = filter(lambda x : x in skills, skillName)
		skillMatch[op.id] = len(intersect)

	print('skill', skillMatch)
	allOps = [op.id for op in allOps]
	resList = []
	for k in skillMatch:
		boost = 0
		if k in sexFilter:
			boost += 1
		if k in opSexFilter:
			boost -= 2
		if k in biwordsOps:
			boost += 2
		skillMatch[k] += boost
		if skillMatch[k] > 0:
			resList.append([skillMatch[k], k])

	resList.sort(reverse = True)
	print('resList', resList)

	return [v for k,v in resList]
	#salary

def skill(query):
	return Skill.objects.filter(name__startswith = query)

def user():
	pass