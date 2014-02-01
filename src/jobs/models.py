#coding=utf-8
from django.db          import models
# from accounts.models    import User, Employer, JobSeeker
from django.utils.safestring import mark_safe
from accounts.models import Employer, JobSeeker
import social_network.models

class JobOpportunity(models.Model):
    user = models.ForeignKey(Employer)
    name = models.CharField(max_length=50)

    MALE = 0
    FEMALE = 1
    BOTH = 2

    SEX_CHOICES = (
        (MALE, 'مرد'),
        (FEMALE, 'زن'),
        (BOTH, 'مرد-زن'),
    )

    sex = models.PositiveSmallIntegerField(choices=SEX_CHOICES , default=BOTH)
    baseSalary = models.IntegerField()
    number = models.IntegerField()
    expireDate = models.DateField()


    def _get_rate(self):
        ratings = social_network.models.RateForOpportunity.objects.all().filter(opportunity__id = self.id)
        frate = 0.0
        for r in ratings:
            frate += r.rate
        if len(ratings) == 0 or frate == 0.0:
            frate = 0
        else:
            frate /= len(ratings)
        return int(round(frate))
    rate = property(_get_rate)

    def __unicode__(self):
        # return mark_safe('<a href="/jobs/' + str(self.id) + '/">' + self.name + '</a>')
        return self.name

class JobOpportunityPage(models.Model):
    opportunity = models.ForeignKey(JobOpportunity, related_name='pages')
    title   = models.CharField(max_length = 100)
    content = models.TextField(null=True, blank=True)
    
class Skill(models.Model):
    name = models.CharField(max_length=50, unique=True)
    user = models.ManyToManyField(JobSeeker, related_name = 'skills', blank = True, null = True)
    opportunity = models.ManyToManyField(JobOpportunity, related_name = 'opSkills', blank = True, null = True)
    class Meta:
        verbose_name = 'مهارت'
        verbose_name_plural = 'مهارت ها'

    def __unicode__(self):
        return self.name



class JobOffer(models.Model):
    jobSeeker = models.ForeignKey(JobSeeker)
    jobOpportunity = models.ForeignKey(JobOpportunity)
    offerDate = models.DateField()

    ACCEPTED = 0
    REJECTED = 1
    PENDING = 2
    STATE_CHOICES = (
        (ACCEPTED , 'قبول شده'),
        (REJECTED ,'رد شده'),
        (PENDING ,'معلق'),
    )
    state = models.PositiveSmallIntegerField(choices=STATE_CHOICES , default=PENDING)

    JOBSEEKER_TO_EMPLOYER = 0
    EMPLOYER_TO_JOBSEEKER = 1
    MODE_CHOICES = (
        (JOBSEEKER_TO_EMPLOYER ,'کارجو به کارفرما'),
        (EMPLOYER_TO_JOBSEEKER ,'کارفرما به کارجو'),
    )
    mode = models.PositiveSmallIntegerField(choices=MODE_CHOICES , default=JOBSEEKER_TO_EMPLOYER)
    date = models.DateField(auto_now_add=True)

