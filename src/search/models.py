from django.db 				import models
from accounts.models 		import *

# Create your models here.
class SearchAgent(models.Model):
	user = models.ForeignKey(JobSeeker)
	start_date = models.DateField()
	min_wage = models.IntegerField(default=0)
	city = models.ManyToManyField(City)
	company_type = models.ManyToManyField(CompanyType)
