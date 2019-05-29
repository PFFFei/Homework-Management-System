from django.contrib import admin
from .models import *

class NoticeAdmin(admin.ModelAdmin):
    list_display = ('title','created')

admin.site.register(Notice,NoticeAdmin)
