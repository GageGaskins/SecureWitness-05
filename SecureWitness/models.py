from django.db import models

# Create your models here.

class Report(models.Model):
    author = models.CharField
    title = models.CharField
    private = models.BooleanField
    timestamp = models.DateTimeField('date published')
    short_description = models.CharField(max_length=100)
    long_description = models.CharField(max_length=500)
    #optional
    #date of event
    #location
    #keywords
    #files