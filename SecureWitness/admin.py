from django.contrib import admin

# Register your models here.

from .models import Report, User, Group, Document, Comment, Folder

admin.site.register(Report)
admin.site.register(User)
admin.site.register(Group)
admin.site.register(Document)
admin.site.register(Comment)
admin.site.register(Folder)