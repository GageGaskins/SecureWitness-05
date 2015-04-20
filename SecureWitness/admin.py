from django.contrib import admin

# Register your models here.

from .models import Report, User, Document, Group

admin.site.register(Report)
admin.site.register(User)
admin.site.register(Document)
admin.site.register(Group)
