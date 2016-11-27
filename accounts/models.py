# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# django import
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

# allauth import
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
        # permission true to superuser
        user.is_active = True
        user.is_admin = True
        user.save(using=self._db)

        return user


# user profile image save path
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
        # checking whether profile image is exists.
        if self.media:
            # local setting
            if settings.DEBUG:
                return '/media/%s' % (self.media)
            # production setting
            else:
                return '%s%s' % (settings.MEDIA_ROOT, self.media)
        else:
            # if social account
            if SocialAccount.objects.filter(user_id=self.id):
                social_user = SocialAccount.objects.filter(user_id=self.id)
                if len(social_user):
                    return "http://graph.facebook.com/{}/picture?width=100&height=100".format(social_user[0].uid)
            return '/static/img/no_profile_hd.png'

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


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


# new seller created
# def new_seller_receiver(sender, instance, created, *args, **kwargs):
#     if created:
#
#
#
#
# post_save.connect(new_seller_receiver, sender=Seller)

BANK_TYPE = (
    ('기업은행', '기업은행'),
    ('국민은행', '국민은행'),
    ('외환은행', '외환은행'),
    ('수협중앙회', '수협중앙회'),
    ('농협중앙회', '농협중앙회'),
    ('우리은행', '우리은행'),
    ('SC제일은행', 'SC제일은행'),
    ('대구은행', '대구은행'),
    ('부산은행', '부산은행'),
    ('광주은행', '광주은행'),
    ('전북은행', '전북은행'),
    ('경남은행', '경남은행'),
    ('한국씨티은행', '한국씨티은행'),
    ('우체국', '우체국'),
    ('하나은행', '하나은행'),
    ('통합신한은행(신한,조흥은행)', '통합신한은행(신한,조흥은행)'),
    ('유안타증권(구 동양증권)', '유안타증권(구 동양증권)'),
    ('현대증권', '현대증권'),
    ('미래에셋증권', '미래에셋증권'),
    ('한국투자증권', '한국투자증권'),
    ('우리투자증권', '우리투자증권'),
    ('하이투자증권', '하이투자증권'),
    ('HMC투자증권', 'HMC투자증권'),
    ('SK증권', 'SK증권'),
    ('대신증권', '대신증권'),
    ('하나대투증권', '하나대투증권'),
    ('굿모닝신한증권', '굿모닝신한증권'),
    ('동부증권', '동부증권'),
    ('유진투자증권', '유진투자증권'),
    ('메리츠증권', '메리츠증권'),
    ('신영증권', '신영증권'),
    ('한국씨티은행(한미은행)', '한국씨티은행 (한미은행)'),
)

class SellerAccount(models.Model):
    seller = models.OneToOneField(Seller)
    account_number = models.CharField(max_length=120, null=True, blank=True)
    account_name = models.CharField(max_length=50, null=True, blank=True)
    bank = models.CharField(max_length=120, null=True, blank=True, choices=BANK_TYPE)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __unicode__(self):
        return self.account_number


class Profit(models.Model):
    seller = models.ForeignKey(Seller)
    money = models.PositiveIntegerField(default=0)
    is_possible_profit = models.BooleanField(default=False)
    is_expect_profit = models.BooleanField(default=False)
    is_complete = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __unicode__(self):
        return self.money
