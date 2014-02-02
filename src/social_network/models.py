#coding=utf-8

from django.db import models

from django.contrib.auth.models import User
from jobs.models import JobOpportunity, JobOffer, Skill
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
    opportunity = models.ForeignKey(JobOpportunity, related_name='comments')
    user = models.ForeignKey(JobSeeker)
    body = models.TextField(max_length=2000)
    time = models.DateTimeField(auto_now_add=True)


class CommentOnEmployer(models.Model):
    user = models.ForeignKey(JobSeeker, related_name='comments_on_employers')
    employer = models.ForeignKey(Employer, related_name = 'comments')
    body = models.TextField(max_length=2000)
    time = models.DateTimeField(auto_now_add=True)


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

    def __str__(self):
        return self.jobSeeker1.user.username + " vs " + self.jobSeeker2.user.username


class Event(models.Model):

    time = models.DateTimeField(auto_now_add=True)
    initial_user = models.ForeignKey(JobSeeker)

    COMMENT_ON_EMPLOYER = 0
    COMMENT_ON_JOB = 1
    FRIENDSHIP = 2
    JOB_OFFER = 3
    JOB_ACCEPT = 4
    ADD_SKILL = 5
    EVENT_TYPE = (
        (COMMENT_ON_EMPLOYER, 'نظر به کارفرما'),
        (COMMENT_ON_JOB, 'نظر به فرصت شغلی'),
        (FRIENDSHIP, 'دوست شدن'),
        (JOB_OFFER, 'درخواست فرصت شغلی'),
        (JOB_ACCEPT, 'قبول فرصت شغلی'),
        (ADD_SKILL, 'اضافه شدن مهارت'),
    )
    type = models.PositiveSmallIntegerField(choices=EVENT_TYPE)

    class Meta:
        ordering = ('-time',)


class Event_JobOffer(Event):
    jobOffer = models.ForeignKey(JobOffer)

    def __init__(self , *args , **kwargs):
        super(Event_CommentOnEmployer , self).__init__(*args , **kwargs)
        self.type = Event.JOB_OFFER

    def summery(self):
        if self.jobOffer.state == JobOffer.EMPLOYER_TO_JOBSEEKER:
            first = self.jobOffer.jobSeeker
            second = self.jobOffer.jobOpportunity.user
        else:
            first = self.jobOffer.jobOpportunity.user
            second = self.jobOffer.jobSeeker
        return dict(
            first = first,
            second = second,
            opp = self.jobOffer.jobOpportunity.name,
            type=self.type,
            # text = self.comment.user.full_name + 'راحع به  '  + self.comment.employer.companyName + "نظر داد ",
            time = self.time
        )

class Event_AddSkill(Event):
    skill = models.ForeignKey(Skill)
    def __init__(self , *args , **kwargs):
        super(Event_CommentOnEmployer , self).__init__(*args , **kwargs)
        self.type = Event.ADD_SKILL

    def summery(self):
        return dict(
            user = self.initial_user,
            skill = self.skill.name,
            time = self.time
        )

class Event_CommentOnEmployer(Event):

    comment = models.ForeignKey(CommentOnEmployer)

    def __init__(self , *args , **kwargs):
        super(Event_CommentOnEmployer , self).__init__(*args , **kwargs)
        self.type = Event.COMMENT_ON_EMPLOYER

    def summery(self):
        return dict(
            user = self.comment.user,
            opp = self.comment.employer.companyName,
            mess = self.comment.body ,
            type=self.type,
            # text = self.comment.user.full_name + 'راحع به  '  + self.comment.employer.companyName + "نظر داد ",
            time = self.time
        )



class Event_CommentOnOpportunity(Event):
    comment = models.ForeignKey(CommentOnOpportunity)

    def __init__(self , *args , **kwargs):
        super(Event_CommentOnOpportunity , self).__init__(*args , **kwargs)
        self.type = Event.COMMENT_ON_JOB

    def summery(self):
        return dict(
            user = self.comment.user,
            opp = self.comment.opportunity.name,
            type=self.type,
            mess = self.comment.body,
            text = self.comment.user.full_name + 'راحع به  '  + self.comment.opportunity.name + "نظر داد ",
            time = self.time
        )


class Event_FriendShip(Event):
    friendShip = models.ForeignKey(FriendShip)

    def __init__(self, *args, **kwargs):
        super(Event_FriendShip, self).__init__(*args, **kwargs)
        self.type = Event.FRIENDSHIP

    def summery(self):
        return dict(
            first = self.friendShip.jobSeeker1.full_name,
            second = self.friendShip.jobSeeker2.full_name,
            type=self.type,
            # text = self.friendShip.jobSeeker1.full_name + ' فعالیت های  '  + self.friendShip.jobSeeker2.full_name + " را دنبال میکند ",
            # text = self.friendShip.jobSeeker1.full_name + 'faalayiat haye ' + self.friendShip.jobSeeker2.full_name + " ra donbal mikonad ",
            time = self.time
        )




