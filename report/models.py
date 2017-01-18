# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# django import
from django.db import models
from django import forms

# app import
from accounts.models import MyUser

report_type_list = (
    ("direct_dealing", "직거래 유도"),
    ("bad_words", "욕설비방"),
    ("illegal_promotion","불법 홍보 유도"),
    ("etc","기타")
)

report_status_list = (
    ("accept","신고접수"),
    ("completed","처리완료")
)

class Report(models.Model):
    writer = models.ForeignKey(MyUser, related_name='report_writer')
    bad_user = models.ForeignKey(MyUser, related_name='report_bad_user')
    type = models.CharField(choices=report_type_list, max_length=20, null=False)
    detail = models.TextField(null=True, blank=True)
    reply = models.TextField(null=True, blank=True)
    status = models.CharField(choices=report_status_list, max_length=15, default="accept")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, null=True)

    def __unicode__(self):
        return str(self.detail)