#-*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from .models import Sns, SocialAnalytics


class TypeItemInline(GenericTabularInline):
    model = SocialAnalytics
    extra = 1


class SnsAdmin(admin.ModelAdmin):
    inlines = [TypeItemInline]

    class Meta:
        model = Sns

admin.site.register(Sns, SnsAdmin)
admin.site.register(SocialAnalytics)