from django.db import models
from accounts.models import Employer


# Create your models here.


class News(models.Model):
    title = models.CharField(max_length=100)
    body = models.CharField(max_length=5000)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date',)


class Advertisement(models.Model):
    employer = models.ForeignKey(Employer)
    description = models.CharField(max_length=3000)
    picture = models.ImageField(upload_to='Ads/')

