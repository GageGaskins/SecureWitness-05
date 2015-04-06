from django.db import models

# Create your models here.

class Report(models.Model):
    author = models.CharField(max_length=120)
    title = models.CharField(max_length=120)
    private = models.BooleanField(default=False)
    author = models.CharField
    title = models.CharField
    private = models.BooleanField
    timestamp = models.DateTimeField(auto_now_add=True)
    short_description = models.CharField(max_length=100)
    long_description = models.CharField(max_length=500)
    user = models.ForeignKey('User')

    def __str__(self):
        return self.title

class User(models.Model):
    name = models.CharField(max_length=30)
    email = models.CharField(max_length=30)
    password = models.CharField(max_length=50)
    admin_status = models.BooleanField(default=False)

    def __str__(self):
        return self.name
