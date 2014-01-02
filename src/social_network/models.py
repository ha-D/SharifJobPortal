#coding=utf-8

from django.db 				import models
# from accounts.models 		import 
from django.contrib.auth.models     import User
from jobs.models					import JobOpportunity
from accounts.models				import *

# Create your models here.

class Message(models.Model):
	sender = models.ForeignKey(User, related_name='sent_messages')
	reciever = models.ForeignKey(User, related_name='recieved_messages')
	subject = models.CharField(max_length=100)
	body = models.TextField(max_length=3000)
	time = models.DateTimeField()

	def __unicode__(self):
		return self.subject

class CommentOnOpportunity(models.Model):
	opportunity = models.ForeignKey(JobOpportunity)
	user = models.ForeignKey(JobSeeker)
	body = models.TextField(max_length=2000)
	time = models.DateTimeField()

class CommentOnEmployer(models.Model):
	user = models.ForeignKey(JobSeeker)
	employer = models.ForeignKey(Employer)
	body = models.TextField(max_length=2000)
	time = models.DateTimeField()

class RateForOpportunity(models.Model):
	opportunity = models.ForeignKey(JobOpportunity)
	user = models.ForeignKey(JobSeeker)
	rate = models.PositiveSmallIntegerField(default=0)

	HARDNESS = 0
	GROWTH_OPPORTUNITY = 1

	FEATURE_CHOICES = (
		(HARDNESS, 'سختی کار'),
		(GROWTH_OPPORTUNITY, 'امکان پیشرفت')
	)

	feature = models.PositiveSmallIntegerField(choices=FEATURE_CHOICES , default=HARDNESS)

class RateForEmployer(models.Model):
	user = models.ForeignKey(JobSeeker)
	employer = models.ForeignKey(Employer)
	rate = models.PositiveSmallIntegerField(default=0)

	ATMOSPHERE = 0
	JOB_SECURITY = 1
	SALARY = 2
	SUPPORT = 3

	FEATURE_CHOICES = (
        (ATMOSPHERE, 'محیط کاری') ,
        (JOB_SECURITY , 'امنیت شغلی'),
        (SALARY , 'حقوق'),
        (SUPPORT, 'پشتیبانی')
    )

	feature = models.PositiveSmallIntegerField(choices=FEATURE_CHOICES , default=SALARY)




