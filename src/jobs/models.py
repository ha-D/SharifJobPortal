#coding=utf-8
from django.db          import models
from accounts.models    import User, Employer, JobSeeker

class JobOpportunity(models.Model):
    user = models.ForeignKey(Employer)

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


class Skill(models.Model):
    name = models.CharField(max_length=50)
    class Meta:
        verbose_name = 'مهارت'
        verbose_name_plural = 'مهارت ها'



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

