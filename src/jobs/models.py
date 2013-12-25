from django.db import models


# Create your models here.
from SharifJobPortal.src.account.models import User, Employer, JobSeeker


class JobOpportunity(models.Model):
    user = models.ForeignKey(Employer)

    MALE = 0
    FEMALE = 1
    BOTH = 2

    SEX_CHOICES = (
        (MALE , 'مرد'),
        (FEMALE , 'زن'),
        (BOTH , 'مرد-زن'),
    )
    sex = models.PositiveSmallIntegerField(choices=SEX_CHOICES , default=BOTH)
    baseSalary = models.IntegerField()
    number = models.IntegerField()
    expireDate = models.DateField()


class Skill(models.Model):
    name = models.CharField(max_length=50)


class JobOffer(models.Model):
    jobSeeker = models.ForeignKey(JobSeeker)
    jobOpportunity = models.ForeignKey(JobOpportunity)
    offerDate = models.DateField()

