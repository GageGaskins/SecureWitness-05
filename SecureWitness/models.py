from django.db import models

# Create your models here.

class Report(models.Model):
    author = models.CharField(max_length=120)
    title = models.CharField(max_length=120)
    private = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    short_description = models.CharField(max_length=100)
    long_description = models.CharField(max_length=500)
    location = models.CharField(max_length=120, default="")
    report_date = models.CharField(max_length=120, default="")
    keywords = models.CharField(max_length=256, default="")
    owner = models.ForeignKey('User')

    def __str__(self):
        return self.title

class User(models.Model):
    name = models.CharField(max_length=30)
    email = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=128)
    admin_status = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Document(models.Model):
    docfile = models.FileField(upload_to='documents/')
