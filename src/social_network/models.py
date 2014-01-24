#coding=utf-8

from django.db import models

from django.contrib.auth.models import User
from jobs.models import JobOpportunity
from accounts.models import *
from django.contrib.contenttypes.models import ContentType
from django.db 				import models
from django.contrib.auth.models     import User
from jobs.models					import JobOpportunity
from accounts.models				import *


class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages')
    reciever = models.ForeignKey(User, related_name='recieved_messages')
    subject = models.CharField(max_length=100)
    body = models.TextField(max_length=3000)
    time = models.DateTimeField(auto_now_add=True)
    unread = models.BooleanField(default=True)

    def __unicode__(self):
        return self.subject
    class Meta:
        ordering = ('-time',)


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

    feature = models.PositiveSmallIntegerField(choices=FEATURE_CHOICES, default=HARDNESS)


class RateForEmployer(models.Model):
    user = models.ForeignKey(JobSeeker)
    employer = models.ForeignKey(Employer)
    rate = models.PositiveSmallIntegerField(default=0)

    ATMOSPHERE = 0
    JOB_SECURITY = 1
    SALARY = 2
    SUPPORT = 3

    FEATURE_CHOICES = (
        (ATMOSPHERE, 'محیط کاری'),
        (JOB_SECURITY, 'امنیت شغلی'),
        (SALARY, 'حقوق'),
        (SUPPORT, 'پشتیبانی')
    )

    feature = models.PositiveSmallIntegerField(choices=FEATURE_CHOICES, default=SALARY)

class FriendShip(models.Model):
    jobSeeker1 = models.ForeignKey(JobSeeker , related_name='requestedFriendShips') #kasi ke invite karde :D
    jobSeeker2 = models.ForeignKey(JobSeeker , related_name='invitedFriendShips')  #kasi ke invite shode!
    start_date = models.DateTimeField(auto_now_add=True)

    PENDING = 0
    ACCEPTED = 1
    FRIENDSHIP_STATUS_CHOICES = (
        (PENDING, 'معلق'),
        (ACCEPTED, 'پذیرفته شده'),
    )
    status = models.PositiveSmallIntegerField(choices=FRIENDSHIP_STATUS_CHOICES, default=PENDING)


class Event(models.Model):

    time = models.DateTimeField(auto_now_add=True)
    initial_user = models.ForeignKey(JobSeeker)

    COMMENT_ON_EMPLOYER = 0
    COMMENT_ON_JOB = 1
    FRIENDSHIP = 2
    JOB_OFFER = 3
    JOB_ACCEPT = 4
    EVENT_TYPE = (
        (COMMENT_ON_EMPLOYER, 'نظر به کارفرما'),
        (COMMENT_ON_JOB, 'نظر به فرصت شغلی'),
        (FRIENDSHIP, 'دوست شدن'),
        (JOB_OFFER, 'درخواست فرصت شغلی'),
        (JOB_ACCEPT, 'قبول فرصت شغلی'),
    )
    type = models.PositiveSmallIntegerField(choices=EVENT_TYPE)


class Event_CommentOnEmployer(Event):

    comment = models.ForeignKey(CommentOnEmployer)

    def __init__(self , *args , **kwargs):
        super(Event_CommentOnEmployer , self).__init__(*args , **kwargs)
        self.type = Event.COMMENT_ON_EMPLOYER


class Event_CommentOnOpportunity(Event):
    comment = models.ForeignKey(CommentOnOpportunity)

    def __init__(self , *args , **kwargs):
        super(Event_CommentOnOpportunity , self).__init__(*args , **kwargs)
        self.type = Event.COMMENT_ON_JOB


class Event_FriendShip(Event):
    friendShip = models.ForeignKey(FriendShip)

    def __init__(self, *args, **kwargs):
        super(Event_FriendShip, self).__init__(*args, **kwargs)
        self.type = Event.FRIENDSHIP

    def summery(self):
        return dict(
            first = self.friendShip.jobSeeker1.full_name(),
            second = self.friendShip.jobSeeker2.full_name(),
            type=self.type,
            text = self.friendShip.jobSeeker1.full_name() + ' donbal mikone faaliataye '  + self.friendShip.jobSeeker2.full_name() + " ro :D ",
            time = self.time
        )




