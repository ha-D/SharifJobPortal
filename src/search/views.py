from accounts.models import JobSeeker
import json
import search
from django.shortcuts            	import render

def opSearch(request):
	user = request.user
	param = request.GET
	query = param.get('q') or ""
	skills = []
	try:
		skills = json.load(param.get('sk'))
	except:
		pass

	if not 'ajax' in param and user.is_authenticated() and len(skills) == 0:
		print("usereeeerrrrrrrrrrrrrrr")
		try:
			print(user.username)
			skillOb = JobSeeker.objects.all().get(user__username = user.username).skills.all()
			# print(len(skillOb))
			for sob in skillOb:
				skills.append(sob.name)
			print(skills)
		except Exception as ex:
		    template = "An exception of type {0} occured. Arguments:\n{1!r}"
		    message = template.format(type(ex).__name__, ex.args)
		    print message
		    skills = []

	search_result = search.opportunity(query, skills)
	context = {'skills' : skills, 'skill_result' : [], 'search_result' : search_result}
	return render(request, 'search/opSearch.html', context)


def skillSearch(request):
	pass


def userSearch(request):
	pass
