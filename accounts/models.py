# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# python import
import os
import shutil
from PIL import Image
import mimetypes
import cStringIO
import boto

# django import
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.core.files.storage import default_storage as storage
from django.core.files import File
from model_utils import FieldTracker

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

    tracker = FieldTracker()

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


    @property
    def is_seller(self):
        seller_exist = Seller.objects.filter(user=self).exists()
        return seller_exist

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


    @property
    def get_thumb_hd_url(self):
        return self.myuserthumbnail_set.get(thumb_type='hd')

    @property
    def get_thumb_sd_url(self):
        return self.myuserthumbnail_set.get(thumb_type='sd')

    @property
    def get_thumb_micro_url(self):
        return self.myuserthumbnail_set.get(thumb_type='micro')

# added
def thumbnail_location(instance, filename):
    if settings.DEBUG:
        return 'avatar/%s/%s' % (instance.myuser.email, filename)
    else:
        return 'avatar/%s/thumb/%s' % (instance.myuser.email, filename)


THUMB_TYPE = (
    ("hd", "HD"),
    ("sd", "SD"),
    ("micro", "Micro"),
)

class MyUserThumbnail(models.Model):
    myuser = models.ForeignKey(MyUser)
    thumb_type = models.CharField(
        max_length=20, choices=THUMB_TYPE, default="hd")
    height = models.CharField(max_length=20, null=True, blank=True)
    width = models.CharField(max_length=20, null=True, blank=True)
    media = models.ImageField(
        width_field="width",
        height_field="height",
        blank=True,
        null=True,
        upload_to=thumbnail_location
    )

    def __unicode__(self):
        if settings.DEBUG:
            return '/media/%s' % (self.media)
        else:
            return '%s%s' % (settings.MEDIA_ROOT, self.media)


def create_new_thumb(image_path, instance, max_length, max_width):
    # 원본 이미지 파일 이름
    filename = os.path.basename(image_path)

    # 원본 이미지 열기
    f = storage.open(image_path, 'r')
    thumb = Image.open(f)

    # 원본 사진의 짧은 길이를 기준으로 리사이즈
    thumb_width, thumb_height = thumb.size
    if thumb_width > thumb_height :
        baseheight = max_width
        hpercent = (baseheight / float(thumb.size[1]))
        wsize = int((float(thumb.size[0]) * float(hpercent)))
        thumb = thumb.resize((wsize, baseheight), Image.ANTIALIAS)
    else :
        basewidth = max_length
        wpercent = (basewidth / float(thumb.size[0]))
        hsize = int((float(thumb.size[1]) * float(wpercent)))
        thumb = thumb.resize((basewidth, hsize), Image.ANTIALIAS)

    # 크롭 이미지 생성
    size = (max_length, max_width)
    crop_img = Image.new('RGBA', size, (255, 255, 255, 0))
    crop_img.paste(
        thumb,
        ((size[0] - thumb.size[0]) // 2, (size[1] - thumb.size[1]) // 2))

    # 썸네일 저장할 디렉토리 위치
    temp_loc = "%sthumb/" % (image_path.split(filename)[0])

    if settings.DEBUG:
        temp_loc = os.path.join(settings.MEDIA_ROOT, temp_loc)

    # 썸네일 폴더 생성
    if not os.path.exists(temp_loc):
        os.makedirs(temp_loc)

    file_name, extends = os.path.splitext(filename)
    temp_file_loc = os.path.join(temp_loc, '%s_%s%s' % (
        filename, instance.thumb_type, extends))
    new_thumbnail_name = "%s_%s%s" % (file_name, instance.thumb_type, extends)

    # 썸네일 저장
    if settings.DEBUG:
        temp_image = open(temp_file_loc, "w")
        crop_img.save(temp_image, "JPEG", optimize=True, progressive=True)
    else:
        try:
            memory_file = cStringIO.StringIO()

            mime = mimetypes.guess_type(new_thumbnail_name)[0]
            plain_ext = mime.split('/')[1]
            crop_img.save(memory_file, plain_ext, optimize=True, progressive=True)

            # S3에 리사이즈한 이미지 업로드
            conn = boto.connect_s3(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY,
                                   host=settings.AWS_S3_HOST)
            bucket = conn.get_bucket(
                settings.AWS_STORAGE_BUCKET_NAME, validate=False)
            k = bucket.new_key('media/' + temp_file_loc)
            k.set_metadata('Content-Type', mime)
            k.set_contents_from_string(memory_file.getvalue())
            k.set_acl("public-read")
            memory_file.close()
        except:
            pass

    # 썸네일 열어서 이미지 필드에 넣기
    try:
        thumb_data = storage.open(temp_file_loc, "r")
        thumb_file = File(thumb_data)

        instance.media.save(new_thumbnail_name, thumb_file)
        shutil.rmtree(temp_loc, ignore_errors=True)
    except:
        pass

    return True


def myuser_post_save_receiver(sender, instance, created, *args, **kwargs):
    if instance.media:
        hd, hd_created = MyUserThumbnail.objects.get_or_create(
            myuser=instance, thumb_type="hd")
        sd, sd_created = MyUserThumbnail.objects.get_or_create(
            myuser=instance, thumb_type="sd")
        micro, micro_created = MyUserThumbnail.objects.get_or_create(
            myuser=instance, thumb_type="micro")

        # 썸네일 크기 3가지로 분류 및 저장
        hd_max = (500, 500)
        sd_max = (350, 350)
        micro_max = (150, 150)

        # 상품 이미지가 저장되어 있는 위치
        image_path = instance.media.name

        if hd_created or instance.tracker.has_changed('media'):
            create_new_thumb(image_path, hd, hd_max[0], hd_max[1])

        if sd_created or instance.tracker.has_changed('media'):
            create_new_thumb(image_path, sd, sd_max[0], sd_max[1])

        if micro_created or instance.tracker.has_changed('media'):
            create_new_thumb(image_path, micro, micro_max[0], micro_max[1])


post_save.connect(myuser_post_save_receiver, sender=MyUser)


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
