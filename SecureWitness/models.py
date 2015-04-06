from django.db import models

# Create your models here.

 class Report(models.Model):
-<<<<<<< HEAD
     author = models.CharField(max_length=120)
     title = models.CharField(max_length=120)
     private = models.BooleanField(default=False)
-=======
     author = models.CharField
     title = models.CharField
     private = models.BooleanField
->>>>>>> dde170b570eb1ab362002a7d88367719f1c5c52c
     timestamp = models.DateTimeField(auto_now_add=True)
     short_description = models.CharField(max_length=100)
     long_description = models.CharField(max_length=500)

    def __str__(self):
        return self.title

class User(models.Model):
    name = models.CharField(max_length=30)
    email = models.CharField(max_length=30)
    password = models.CharField(max_length=50)
    admin_status = models.BooleanField(default=False)

    def __str__(self):
        return self.name
>>>>>>> 611322a6987f92be276ca6f868482e1803e16634
