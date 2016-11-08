# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# python import
import os
import shutil
from PIL import Image
import random
import mimetypes
import re
import cStringIO
import boto

# django import
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.core.files import File
from django.core.files.storage import default_storage as storage
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import post_save

# app import
from django_summernote import fields as summer_fields
from accounts.models import Seller


def upload_product_image(instance, filename):
    return "product/%s/%s" % (instance, filename)


class ProductQueryset(models.query.QuerySet):
    def active(self):
        return self.filter(is_active=True)


class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQueryset(self.model, using=self._db)

    def active(self):
        return self.get_queryset().active()


class Product(models.Model):
    seller = models.ForeignKey(Seller, null=False, blank=False)
    title = models.CharField(max_length=120, blank=False)
    image = models.ImageField(upload_to=upload_product_image, null=True, blank=True)
    tags = GenericRelation("ProductTag", null=True, blank=True)
    url = GenericRelation("SnsUrl", null=True, blank=True)
    type = GenericRelation("SnsType", null=True, blank=True)
    target = GenericRelation("ProductTarget", null=True, blank=True)
    influence = models.CharField(max_length=255, null=True, blank=True)
    required = models.TextField(null=True, blank=True)
    description = summer_fields.SummernoteTextField(null=True, blank=True)
    refund = models.TextField(null=True, blank=True)
    command = models.TextField(null=True, blank=True)
    rating = models.DecimalField(default=0.00, decimal_places=2, max_digits=3)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    objects = ProductManager()

    def __unicode__(self):
        return u'%s' % (self.title)

    @property
    def get_absolute_url(self):
        return reverse('product_detail', kwargs={"product_id": self.id})

    @property
    def get_image_url(self):
        if self.image:
            if settings.DEBUG:
                return '/media/%s' % (self.image)
            else:
                return '%s%s' % (settings.MEDIA_ROOT, self.image)
        else:
            return None

    @property
    def get_thumb_hd_url(self):
        return self.productthumbnail_set.get(thumb_type='hd')

    @property
    def get_thumb_sd_url(self):
        return self.productthumbnail_set.get(thumb_type='sd')

    @property
    def get_thumb_micro_url(self):
        return self.productthumbnail_set.get(thumb_type='micro')


def thumbnail_location(instance, filename):
    if settings.DEBUG:
        return 'product/%s/%s' % (instance.product.title, filename)
    else:
        return 'product/%s/thumb/%s' % (instance.product.title, filename)


THUMB_TYPE = (
    ("hd", "HD"),
    ("sd", "SD"),
    ("micro", "Micro"),
)


class ProductThumbnail(models.Model):
    product = models.ForeignKey(Product)
    thumb_type = models.CharField(max_length=20, choices=THUMB_TYPE, default="hd")
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

    # 썸네일 사이즈 & 리사이즈
    size = (max_length, max_width)
    thumb.thumbnail(size, Image.ANTIALIAS)

    # 썸네일 저장할 디렉토리 위치
    temp_loc = "%sthumb/" % (image_path.split(filename)[0])

    if settings.DEBUG:
        temp_loc = os.path.join(settings.MEDIA_ROOT, temp_loc)


    # 썸네일 폴더 생성
    if not os.path.exists(temp_loc):
        os.makedirs(temp_loc)


    file_name, extends = os.path.splitext(filename)
    temp_file_loc = os.path.join(temp_loc, '%s_%s%s' % (filename, instance.thumb_type, extends))
    new_thumbnail_name = "%s_%s%s" % (file_name, instance.thumb_type, extends)

    # 썸네일 저장
    if settings.DEBUG:
        temp_image = storage.open(temp_file_loc, "w")
        thumb.save(temp_image, "JPEG", optimize=True, progressive=True)
    else:
        try:
            memory_file = cStringIO.StringIO()

            mime = mimetypes.guess_type(new_thumbnail_name)[0]
            plain_ext = mime.split('/')[1]
            thumb.save(memory_file, plain_ext, optimize=True, progressive=True)

            # S3에 리사이즈한 이미지 업로드
            conn = boto.connect_s3(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY,
                                   host=settings.AWS_S3_HOST)
            bucket = conn.get_bucket(settings.AWS_STORAGE_BUCKET_NAME, validate=False)
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


def product_post_save_receiver(sender, instance, created, *args, **kwargs):
    if instance.image:
        hd, hd_created = ProductThumbnail.objects.get_or_create(product=instance, thumb_type="hd")
        sd, sd_created = ProductThumbnail.objects.get_or_create(product=instance, thumb_type="sd")
        micro, micro_created = ProductThumbnail.objects.get_or_create(product=instance, thumb_type="micro")

        # 썸네일 크기 3가지로 분류 및 저장
        hd_max = (500, 500)
        sd_max = (350, 350)
        micro_max = (150, 150)

        # 상품 이미지가 저장되어 있는 위치
        image_path = instance.image.name

        if hd_created:
            create_new_thumb(image_path, hd, hd_max[0], hd_max[1])

        if sd_created:
            create_new_thumb(image_path, sd, sd_max[0], sd_max[1])

        if micro_created:
            create_new_thumb(image_path, micro, micro_max[0], micro_max[1])


post_save.connect(product_post_save_receiver, sender=Product)


class Variation(models.Model):
    product = models.ForeignKey(Product)
    title = models.CharField(max_length=120)
    price = models.PositiveIntegerField(default=0)
    day = models.PositiveIntegerField(default=0)
    sale_price = models.PositiveIntegerField(null=True, blank=True)
    is_default = models.BooleanField(default=False)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.title

    @property
    def get_price(self):
        if self.sale_price is not None:
            return self.sale_price
        else:
            return self.price


product_type = (
    ('all', "전체"),
    ("it", "IT/인터넷"),
    ("fasion", "패션/뷰티"),
    ("travel", "여행/숙박"),
    ("game", "게임"),
    ("car", "자동차"),
    ("financial", "재테크/금융"),
    ("study", "취업/학업"),
    ("baby", "육아"),
    ("pet", "반려동물"),
    ("media", "미디어/영화"),
    ("interior", "인테리어"),
    ("food", "맛집/식품"),
    ("music", "음악"),
    ("diet", "다이어트"),
    ("health", "리빙/건강"),
    ("life", "일상/생활"),
    ("picture", "사진"),
    ("love", "결혼/연애"),
    ("sports", "스포츠/레저"),
)


class ProductTag(models.Model):
    tag = models.CharField(choices=product_type, max_length=15, null=False)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    def __unicode__(self):
        return self.tag


sns_type = (
    ('all', "전체"),
    ("blog", "블로그"),
    ("facebook", "페이스북"),
    ("instagram", "인스타그램"),
    ("kakaostroy", "카카오스토리"),
    ("twitter", "트위터"),
    ("cafe", "카페"),
    ("afreecatv", "아프리카TV"),
    ("pholar", "폴라"),
    ("etc", "기타"),
)


class SnsType(models.Model):
    type = models.CharField(choices=sns_type, max_length=15, null=False)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    def __unicode__(self):
        return self.type


product_target = (
    ('all', "전 연령"),
    ("10", "10대"),
    ("20", "20대"),
    ("30", "30대"),
    ("40", "40대 이상"),
    ("gender", "남여 모두"),
    ("male", "남성"),
    ("female", "여성"),
)


class ProductTarget(models.Model):
    target = models.CharField(choices=product_target, max_length=15, null=False)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    def __unicode__(self):
        return self.target


class SnsUrl(models.Model):
    url = models.URLField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    def __unicode__(self):
        return self.url


        # def new_rating_receiver(sender, instance, created, *args, **kwargs):
        #     seller = Seller.objects.get(id=instance.seller.id)
        #
        #     rating = seller.rating
        #
        #     rating = (rating + instance.rating) / 2
        #     seller.rating = rating
        #     seller.save()
        #
        #
        # post_save.connect(new_rating_receiver, sender=Product)
