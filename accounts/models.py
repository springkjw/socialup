# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import requests
import json
import urllib

from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from allauth.socialaccount.models import SocialAccount


class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('이메일은 필수 항목입니다.')

        user = self.model(
            email=self.normalize_email(email)
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email,
            password=password
        )
        user.is_active = True
        user.is_admin = True
        user.save(using=self._db)
        return user


def download_profile_location(instance, filename):
    return "avatar/%s/%s" % (instance, filename)


class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    media = models.ImageField(
        null=True,
        blank=True,
        upload_to=download_profile_location
    )
    description = models.TextField(null=True, blank=True)
    name = models.CharField(max_length=10, null=True, blank=True)
    phone = models.CharField(max_length=12, null=True, blank=True)
    access_token = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'

    def __unicode__(self):
        return self.email

    def get_short_name(self):
        if self.name:
            return self.name
        else:
            return self.email.split('@')[0]

    @property
    def is_staff(self):
        return self.is_admin

    @property
    def get_avatar(self):
        if self.media:
            if settings.DEBUG:
                return '/media/%s' % (self.media)
            else:
                return '%s%s' % (settings.MEDIA_ROOT, self.media)
        else:
            if SocialAccount.objects.filter(user_id=self.id):
                social_user = SocialAccount.objects.filter(user_id=self.id)
                if len(social_user):
                    return "http://graph.facebook.com/{}/picture?width=100&height=100".format(social_user[0].uid)
            return '/static/img/no_profile.png'

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


def new_user_receiver(sender, instance, created, *args, **kwargs):
    if not instance.access_token:
        # UID = urllib.quote(instance.email, safe='')
        UID = instance.email

        url = 'https://api.sendbird.com/v3/users'
        headers = {
            "Api-Token": settings.SD_API_TOKEN
        }
        data = {
            "user_id": UID,
            "nickname": instance.get_short_name(),
            "profile_url": instance.get_avatar,
            "issue_access_token": True
        }

        req = requests.post(url, data=json.dumps(data), headers=headers)

        res = json.loads(req.content)

        print res

        # 이미 sendbird에 user가 등록되어 있는 경우
        if res['code'] and res['code'] == 400202:
            url_r = 'https://api.sendbird.com/v3/users/%s' % (UID)

            req_r = requests.get(url_r, headers=headers)

            res_r = json.loads(req_r.content)

            access_token_r = res_r['access_token']

            # access_token이 있는 경우
            if access_token_r:
                instance.access_token = str(access_token_r)
                instance.save()
            # access_token이 없는 경우
            else:
                url_a = 'https://api.sendbird.com/v3/users/%s' % (UID)
                data_a = {
                    "issue_access_token": True
                }
                req_a = requests.put(url_a, data=json.dumps(data_a), headers=headers)
                res_a = json.loads(req_a.content)
                access_token_a = res_a['access_token']

                instance.access_token = str(access_token_a)
                instance.save()
        # sendbird에 user를 처음 등록하는 경우
        else:
            access_token = res['access_token']

            if access_token:
                instance.access_token = str(access_token)
                instance.save()


post_save.connect(new_user_receiver, sender=MyUser)


class Seller(models.Model):
    user = models.OneToOneField(MyUser)
    maxWorking = models.PositiveIntegerField(default=0)
    description = models.TextField(null=True, blank=True)
    phone = models.CharField(max_length=12, null=False, blank=False)
    rating = models.DecimalField(default=0.00, decimal_places=2, max_digits=3)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __unicode__(self):
        user = self.user
        return str(user).split("@")[0]
