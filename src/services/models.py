from django.db import models


# Create your models here.
from SharifJobPortal.src.accounts.models import Employer


class News(models.Model):
    title = models.CharField('خبر' , max_length=100)
    body = models.CharField('' , max_length=5000)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date',)
        verbose_name = 'خبر'
        verbose_name_plural = 'اخبار'


class Advertisement(models.Model):
    employer = models.ForeignKey(Employer)
    description = models.CharField(3000)
    picture = models.ImageField(upload_to='Ads/')

