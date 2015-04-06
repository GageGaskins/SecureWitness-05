from django.contrib import admin

# Register your models here.

from .models import Report, User

admin.site.register(Report)
admin.site.register(User)