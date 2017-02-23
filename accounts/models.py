# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# python import
import os
import shutil
from PIL import Image
import mimetypes
import cStringIO
import boto
import random

# django import
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.core.files.storage import default_storage as storage
from django.core.files import File
from model_utils import FieldTracker
from django.core.urlresolvers import reverse

# allauth import
from allauth.socialaccount.models import SocialAccount
from allauth.account.models import EmailAddress


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

        email_conform = EmailAddress.objects.create(
            user=user,
            email=email
        )
        email_conform.verified = True
        email_conform.primary = True
        email_conform.save()

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
    description = models.TextField(null=True, blank=True, default="")
    name = models.CharField(max_length=10, null=True, blank=True, default="")
    phone = models.CharField(max_length=13, null=True, blank=True, default="")
    sex = models.CharField(choices=(("male", "남자"), ("female", "여자")), max_length=15, null=True)
    address = models.CharField(max_length=15, null=True, default="")
    job = models.CharField(max_length=15, null=True, blank=True, default="")
    birth_year = models.PositiveIntegerField(null=True)

    agree_purchase_info_email = models.BooleanField(default=True)
    agree_purchase_info_SMS = models.BooleanField(default=False)
    agree_selling_info_email = models.BooleanField(default=True)
    agree_selling_info_SMS = models.BooleanField(default=True)
    agree_marketing_info_email = models.BooleanField(default=True)
    agree_marketing_info_SMS = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    # 필드 업데이트 감지를 위한 트래커
    tracker = FieldTracker()

    USERNAME_FIELD = 'email'

    def __unicode__(self):
        return self.email

    def get_short_name(self):
        if self.name:
            return self.name
        else:
            return self.email.split('@')[0]

    def get_email_id(self):
        return self.email.split('@')[0]

    @property
    def is_staff(self):
        return self.is_admin

    @property
    def get_avatar(self):
        # checking whether profile image is exists.
        if self.media:
            try:
                thumbnail = MyUserThumbnail.objects.get(myuser=self, thumb_type='hd')
                # local setting
                if settings.DEBUG:
                    return '/media/%s' % (thumbnail.media)
                # production setting
                else:
                    return '%s%s' % (settings.MEDIA_ROOT, thumbnail.media)
            except:
                pass

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
            # no profile
            else:
                # 유저 이메일 주소에 따라 1~3 숫자로 변환
                pseudo_random_num = int(int(self.email.encode('hex'), 16) % 3) + 1
                random_profile = static('img/no_profile_' + str(pseudo_random_num) + '.png')
                return random_profile

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
    if thumb_width > thumb_height:
        baseheight = max_width
        hpercent = (baseheight / float(thumb.size[1]))
        wsize = int((float(thumb.size[0]) * float(hpercent)))
        thumb = thumb.resize((wsize, baseheight), Image.ANTIALIAS)
    else:
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
    # # 새 아이디를 만들었을 경우 랜덤 토끼 프로필 이미지 저장
    # if created:
    #     # 원본 이미지 파일 이름
    #     random_img_path = random.choice(
    #         ['static/img/no_profile_1.png', 'static/img/no_profile_2.png', 'static/img/no_profile_3.png'])
    #     filename = os.path.basename(random_img_path)
    #     thumb = Image.open(random_img_path)
    #
    #     # 저장할 디렉토리 위치
    #     temp_loc = "%s/" % (random_img_path.split(filename)[0])
    #
    #     if settings.DEBUG:
    #         temp_loc = os.path.join(settings.MEDIA_ROOT, temp_loc)
    #
    #     # 폴더 생성
    #     if not os.path.exists(temp_loc):
    #         os.makedirs(temp_loc)
    #
    #     file_name, extends = os.path.splitext(filename)
    #     temp_file_loc = os.path.join(temp_loc, '%s_%s' % (
    #         filename, extends))
    #     new_thumbnail_name = "%s_%s" % (file_name, extends)
    #
    #     # 저장
    #     if settings.DEBUG:
    #         temp_image = open(temp_file_loc, "w")
    #         thumb.save(temp_image, "JPEG", optimize=True, progressive=True)
    #
    #     else:
    #         try:
    #             memory_file = cStringIO.StringIO()
    #
    #             mime = mimetypes.guess_type(new_thumbnail_name)[0]
    #             plain_ext = mime.split('/')[1]
    #             thumb.save(memory_file, plain_ext, optimize=True, progressive=True)
    #
    #             # S3에 이미지 업로드
    #             conn = boto.connect_s3(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY,
    #                                    host=settings.AWS_S3_HOST)
    #             bucket = conn.get_bucket(
    #                 settings.AWS_STORAGE_BUCKET_NAME, validate=False)
    #             k = bucket.new_key('media/' + temp_file_loc)
    #             k.set_metadata('Content-Type', mime)
    #             k.set_contents_from_string(memory_file.getvalue())
    #             k.set_acl("public-read")
    #             memory_file.close()
    #         except:
    #             pass
    #
    #     # 저장된 파일 이미지 필드에 넣기
    #     try:
    #         thumb_data = storage.open(temp_file_loc, "r")
    #         thumb_file = File(thumb_data)
    #
    #         instance.media.save(new_thumbnail_name, thumb_file)
    #         shutil.rmtree(temp_loc, ignore_errors=True)
    #     except:
    #         pass

    # 썸네일 3가지 크기로 저장
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

seller_type_list = (
    ("individual", "개인"),
    ("personal_business", "개인사업자"),
    ("corporate_business", "법인사업자"),
    ("confirming_status", "확인중")
)

def download_seller_account_location(instance, filename):
    return "account_copy/%s/%s" % (instance, filename)

def download_seller_license_location(instance, filename):
    return "business_license/%s/%s" % (instance, filename)

class Seller(models.Model):
    user = models.OneToOneField(MyUser)
    maxWorking = models.PositiveIntegerField(default=0)
    description = models.TextField(null=True, blank=True)
    phone = models.CharField(max_length=12, null=False, blank=False)
    rating = models.DecimalField(default=0.00, decimal_places=2, max_digits=3)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    total_num_heart = models.PositiveIntegerField(default=0)

    type = models.CharField(choices=seller_type_list, max_length=20, null=True, blank=False, default="individual")
    company_name = models.CharField(max_length=12, null=True, blank=True, default="")
    representative_name = models.CharField(max_length=12, null=True, blank=True, default="")
    corporate_number = models.CharField(max_length=12, null=True, blank=False, default="")
    business_field = models.CharField(max_length=12, null=True, blank=True, default="")
    company_type = models.CharField(max_length=12, null=True, blank=True, default="")
    business_license = models.ImageField(
        blank=True,
        null=True,
        upload_to=download_seller_license_location
    )
    account_copy = models.ImageField(
        blank=True,
        null=True,
        upload_to=download_seller_account_location
    )

    # seller_account
    # account_number = models.CharField(max_length=120, null=True, blank=True)
    # account_name = models.CharField(max_length=50, null=True, blank=True)
    # bank = models.CharField(max_length=120, null=True, blank=True, choices=BANK_TYPE)
    # timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)



    def __unicode__(self):
        user = self.user
        return str(user).split("@")[0]

    @property
    def get_absolute_url(self):
        return reverse('account_detail', kwargs={"seller_id": self.id})

    def type_in_korean(self):
        type_in_korean = {"individual": "개인",
                          "personal_business": "개인사업자",
                          "corporate_business": "법인사업자", }
        return type_in_korean[self.type]


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
    account_number = models.CharField(max_length=120, null=True, blank=True, default="")
    account_name = models.CharField(max_length=50, null=True, blank=True, default="")
    bank = models.CharField(max_length=120, null=True, blank=True, choices=BANK_TYPE, default="")
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __unicode__(self):
        return self.account_number


# profit_type_list = (
#     ("possible_profit", "possible_profit"),
#     ("expect_profit", "expect_profit"),
#     ("requested_profit", "requested_profit"),
#     ("completed_profit", "completed_profit")
# )
#
#
# class Profit(models.Model):
#     seller = models.ForeignKey(Seller)
#     money = models.IntegerField(default=0)
#     type = models.CharField(choices=profit_type_list, max_length=20, null=True)
#     timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
#
#     def __unicode__(self):
#         return str(self.money)


withdrawal_status_list = (
    ("request", "출금요청"),
    ("completed", "출금완료"),
    ("rejected", "출금거절")
)


class Withdrawal(models.Model):
    seller = models.ForeignKey(Seller)
    money = models.PositiveIntegerField(default=0)
    status = models.CharField(choices=withdrawal_status_list, max_length=15, null=True)
    reject_reason = models.CharField(max_length=255, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    timestamp = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __unicode__(self):
        return str(self.money)

    def status_in_korean(self):
        statuses = {'request': '출금요청',
                    'completed': '출금완료',
                    'rejected': '출금거절'}
        return statuses[self.status]


def withdrawal_post_save_receiver(sender, instance, created, *args, **kwargs):
    if created and instance.status == "request":
        from billing.models import Point, PointHistory
        user = instance.seller.user
        try:
            # 출금 요청액만큼 point 차감
            point = Point.objects.get(user=user)
            point.point= point.point - instance.money
            point.save()
        except:
            raise ValueError('포인트 차감에 문제가 발생했습니다.')

        try:
            # 포인트 history 추가
            h = PointHistory(
                user=instance.seller.user,
                amount=-instance.money,
                type='withdraw_request',
                detail='출금요청',
            )
            h.save()
        except:
            raise ValueError('포인트 히스토리 추가에 문제가 발생했습니다.')


post_save.connect(withdrawal_post_save_receiver, sender=Withdrawal)
