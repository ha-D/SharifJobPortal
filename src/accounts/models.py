#coding=utf-8

from django.db                      import models
from django.contrib.auth.models     import User

from polymorphic                    import PolymorphicModel
# from social_network.models          import RateForEmployer
import social_network.models 
# from jobs.models                    import Skill

class City(models.Model):
    name = models.CharField(max_length=20)
    def __unicode__(self):
        return self.name

class UserProfile(models.Model):
    address = models.CharField(max_length=300)
    postalCode = models.CharField(max_length=15)
    phoneNumber = models.CharField(max_length=15)
    image = models.ImageField(null = True, blank = True, upload_to="avatar")
    city = models.ForeignKey(City)
    personalPage = models.OneToOneField('accounts.PersonalPage' , unique=True, null=True, blank=True)
    
    user = models.OneToOneField(User , unique=True)

    def is_jobseeker(self):
        pass

    def is_employer(self):
        return not self.is_jobseeker()

    class Meta:
        abstract = True

    def __unicode__(self):
        return self.user.username

class CompanyType(models.Model):
    PUBLIC = 0
    PRIVATE = 1
    SEMI_PRIVATE = 2

    COMPANY_TYPE_CHOICES = (
        (PUBLIC , u'دولتی') ,
        (PRIVATE , u'خصوصی'),
        (SEMI_PRIVATE , u'نیمه خصوصی'),
    )

    companyType = models.PositiveSmallIntegerField(choices=COMPANY_TYPE_CHOICES , default=PUBLIC)

    def __unicode__(self):
        for s,t in self.COMPANY_TYPE_CHOICES:
            print(s,t)
            if self.companyType == s:
                return t


class Employer(UserProfile):
    companyName = models.CharField(max_length=30)
    
    companyType = models.ForeignKey(CompanyType)
    
    registrationNumber = models.CharField(max_length=20)
    contactEmail = models.EmailField()
    webSite = models.URLField()
    establishDate = models.DateField()
    
    def _get_rate(self):
        ratings = social_network.models.RateForEmployer.objects.all().filter(employer__user__username = self.user.username)
        frate = 0.0
        for r in ratings:
            frate += r.rate
        if len(ratings) == 0 or frate == 0.0:
            frate = 0
        else:
            frate = frate / len(ratings)
        return int(round(frate))
    rate = property(_get_rate)

        

    def is_jobseeker(self):
        return False


class JobSeeker(UserProfile):
    birthDate = models.DateField(null=True, blank=True)

    MALE = 0
    FEMALE = 1
    SEX_CHOICES = (
        (MALE , 'مرد'),
        (FEMALE , 'زن'),
    )
    sex = models.PositiveSmallIntegerField(choices=SEX_CHOICES , default=FEMALE)

    PART_TIME = 0
    FULL_TIME = 1
    UNEMPLOYED = 2
    JOB_STATUS_CHOICES = (
        (PART_TIME , 'پاره وقت'),
        (FULL_TIME , 'تمام وقت'),
        (UNEMPLOYED , 'بیکار'),
    )
    job_status = models.PositiveSmallIntegerField(choices=JOB_STATUS_CHOICES , default=UNEMPLOYED, null=True, blank=True)

    cv = models.FileField(upload_to="cv", null=True, blank=True)
    

    def is_jobseeker(self):
        return True

class PersonalPage(models.Model):
    aboutMe = models.TextField(max_length=3000)
    background = models.TextField(max_length=3000)
    projects = models.TextField(max_length=3000)


class Record(models.Model):
    user = models.ForeignKey(User)
    startDate = models.DateField()
    endDate = models.DateField()
    position = models.CharField(max_length=20)
    companyName = models.CharField(max_length=30)
