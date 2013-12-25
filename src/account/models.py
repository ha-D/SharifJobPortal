from django.db import models


# Create your models here.

class User(models.User):

    address = models.CharField(max_length=300)
    postalCode = models.CharField(max_length=15)
    phoneNumber = models.CharField(max_length=15)
    image = models.URLField()
    city = models.CharField(max_length=20)
    personalPage = models.ForeignKey(PersonalPage , unique=True)




class Employer(models.Model):
    companyName = models.CharField(max_length=30)
    PUBLIC = 0
    PRIVATE = 1
    SEMI_PRIVATE = 2

    COMPANY_TYPE_CHOICES = (
        (PUBLIC , 'دولتی') ,
        (PRIVATE , 'خصوصی'),
        (SEMI_PRIVATE , 'نیمه خصوصی'),
    )
    companyType = models.PositiveSmallIntegerField( choices=COMPANY_TYPE_CHOICES , default=PUBLIC)
    registrationNumber = models.CharField(max_length=20)
    contactEmail = models.EmailField()
    webSite = models.URLField()
    establishDate = models.DateField()
    user = models.ForeignKey(User , unique=True)


class JobSeeker(models.Model):
    birthDate = models.DateField()

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
    job_status = models.PositiveSmallIntegerField(choices=JOB_STATUS_CHOICES , default=UNEMPLOYED)

    cv = models.URLField()
    user = models.ForeignKey(User , unique=True)


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

