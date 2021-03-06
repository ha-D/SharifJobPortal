#coding=utf-8
from django.db                      import models
from django.contrib.auth.models     import User
from django.utils.safestring import mark_safe
# from social_network.models          import RateForEmployer
import social_network.models 
# from jobs.models                    import Skill

class City(models.Model):
    name = models.CharField(max_length=20)
    def __unicode__(self):
        return self.name

class UserProfile(models.Model):
    address = models.CharField(max_length=300, verbose_name="آدرس")
    postalCode = models.CharField(max_length=15, verbose_name="کد پستی")
    phoneNumber = models.CharField(max_length=15, verbose_name="شماره تلفن")
    image = models.ImageField(null = True, blank = True, upload_to="avatar", verbose_name="عکس", default="noimage.jpg")
    city = models.ForeignKey(City, verbose_name="شهر")

    profilePage = models.CharField(max_length=20, null=True, blank=True)

    user = models.OneToOneField(User , unique=True)

    def _username(self):
        return self.user.username
    def _first_name(self):
        return self.user.first_name
    def _last_name(self):
        return self.user.last_name
    def _full_name(self):
        return '%s %s' % (self.first_name, self.last_name)

    username   = property(_username)
    first_name = property(_first_name)
    last_name  = property(_last_name)
    full_name  = property(_full_name)

    def is_jobseeker(self):
        pass

    def is_employer(self):
        return not self.is_jobseeker()

    class Meta:
        abstract = True

    def __unicode__(self):
        return self.user.username

class CompanyType(models.Model):
    # PUBLIC = 0
    # PRIVATE = 1
    # SEMI_PRIVATE = 2

    # COMPANY_TYPE_CHOICES = (
    #     (PUBLIC , u'دولتی') ,
    #     (PRIVATE , u'خصوصی'),
    #     (SEMI_PRIVATE , u'نیمه خصوصی'),
    # )

    # companyType = models.PositiveSmallIntegerField(choices=COMPANY_TYPE_CHOICES , default=PUBLIC)

    companyType = models.CharField(max_length=30)
    def __unicode__(self):
        # for s,t in self.COMPANY_TYPE_CHOICES:
        #     print(s,t)
        #     if self.companyType == s:
        #         return t
        return self.companyType


class Employer(UserProfile):
    companyName = models.CharField(max_length=30, verbose_name="نام شرکت")
    
    companyType = models.ForeignKey(CompanyType, verbose_name="نوع شرکت")
    
    registrationNumber = models.CharField(max_length=20, verbose_name="شماره ثبت")
    contactEmail = models.EmailField(verbose_name="آدرسی الکترونیکی ارتباط")
    webSite = models.URLField(verbose_name="تارنمای شرکت")
    establishDate = models.DateField(verbose_name="تاریخ تاسیس")
    
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

    def __unicode__(self):
        # Don't do this!!, problems with links in admin
        # return mark_safe('<a href="/employer/' + self.user.username + '/">' + self.companyName + '</a>')
        return self.companyName

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
        (PART_TIME , u'پاره وقت'),
        (FULL_TIME , u'تمام وقت'),
        (UNEMPLOYED , u'بیکار'),
    )
    job_status = models.PositiveSmallIntegerField(choices=JOB_STATUS_CHOICES , default=UNEMPLOYED, null=True, blank=True, verbose_name=u'وضعیت شغلی')
    cv = models.FileField(upload_to="cv", null=True, blank=True, verbose_name=u'کارنامک کاری')
    friends = models.ManyToManyField('JobSeeker' , through='social_network.FriendShip' , related_name='friends2')

    NO_ACCESS   = 0
    PART_ACCESS = 1
    ALL_ACCESS  = 2
    JOBSEEKER_PRIVACY_CHOICES = (
        (NO_ACCESS,     u'هیچ کارجویی'),
        (PART_ACCESS, u'کارجویان دوست'),
        (ALL_ACCESS, u'همه کارجویان'),
    )
    EMPLOYER_PRIVACY_CHOICES = (
        (NO_ACCESS,     u'هیچ کارفرمایی'),
        (PART_ACCESS, u'کارفرمایانی که درخواست استخدام داده‌اید'),
        (ALL_ACCESS, u'همه کارفرمایان'),
    )
    access_profile_public    = models.BooleanField(default=True)
    access_profile_jobseeker = models.PositiveSmallIntegerField(choices=JOBSEEKER_PRIVACY_CHOICES, default=PART_ACCESS, blank=True)
    access_profile_employer  = models.PositiveSmallIntegerField(choices=EMPLOYER_PRIVACY_CHOICES, default=PART_ACCESS, blank=True)
    access_cv_public         = models.BooleanField(default=True)
    access_cv_jobseeker      = models.PositiveSmallIntegerField(choices=JOBSEEKER_PRIVACY_CHOICES, default=PART_ACCESS, blank=True)
    access_cv_employer       = models.PositiveSmallIntegerField(choices=EMPLOYER_PRIVACY_CHOICES, default=PART_ACCESS, blank=True)

    def _sex_name(self):
        return self.SEX_CHOICES[self.sex][1]
    def _job_status_name(self):
        return self.JOB_STATUS_CHOICES[self.job_status][1]
    sex_name = property(_sex_name)
    job_status_name = property(_job_status_name)

    def __unicode__(self):
        # Don't do this!!, problems with links in admin
        # return mark_safe('<a href="/user/' + self.user.username + '/">' + self.user.first_name + ' ' + self.user.last_name + '</a>')
        return self.user.first_name + ' ' + self.user.last_name

    def is_jobseeker(self):
        return True




class PersonalPage(models.Model):
    user    = models.ForeignKey(User, related_name='pages')
    title   = models.CharField(max_length = 100)
    content = models.TextField(null=True, blank=True)

class CompanyImage(models.Model):
    employer = models.ForeignKey(Employer, related_name="images")
    image = models.ImageField(upload_to='employer_pics/', default='noimage.jpg')

class Record(models.Model):
    user = models.ForeignKey(User)
    startDate = models.DateField()
    endDate = models.DateField()
    position = models.CharField(max_length=20)
    companyName = models.CharField(max_length=30)
