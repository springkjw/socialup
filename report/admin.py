from django.contrib import admin
from .models import Report

class ReportAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'type', 'status')
    list_filter = ('status',)

admin.site.register(Report, ReportAdmin)
