from django.contrib import admin

# Register your models here.

from .models import Report, User, Group, Document

admin.site.register(Report)
admin.site.register(User)
admin.site.register(Group)
admin.site.register(Document)