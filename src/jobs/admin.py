from django.contrib 	import admin
from jobs.models import JobOpportunity, Skill, JobOffer

admin.site.register(JobOpportunity)
admin.site.register(Skill)
admin.site.register(JobOffer)
