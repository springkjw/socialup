# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from accounts.models import MyUser
from billing.models import Order


def download_file_location(instance, filename):
    return "contact/%s/%s" % (instance, filename)


USER_TYPE = [('user', '구매회원'),
             ('seller', '판매회원')]


class Contact(models.Model):
    user = models.ForeignKey(MyUser)
    user_type = models.CharField(max_length=50, choices=USER_TYPE, default='user')
    title = models.CharField(max_length=255, null=False, blank=False)
    order_num = models.ForeignKey(Order, null=True, blank=True)
    message = models.TextField()
    response_message = models.TextField()
    status = models.BooleanField(default=False)
    file = models.FileField(
        null=True,
        blank=True,
        upload_to=download_file_location
    )
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __unicode__(self):
        return self.title
