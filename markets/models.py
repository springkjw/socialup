# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# django import
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.db import models
from model_utils import FieldTracker

# app import
from django_summernote import fields as summer_fields
from accounts.models import Seller


class ProductQueryset(models.query.QuerySet):
    def active(self):
        return self.filter(is_now_selling=True)


class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQueryset(self.model, using=self._db)

    def active(self):
        return self.get_queryset().active()

sns_type_list = (
    #('all', "전체"),
    ("blog", "블로그"),
    ("facebook", "페이스북"),
    ("instagram", "인스타그램"),
    ("kakaostory", "카카오스토리"),
    #("twitter", "트위터"),
    #("cafe", "카페"),
    #("afreecatv", "아프리카TV"),
    #("pholar", "폴라"),
    #("etc", "기타"),
)

sns_additional_info_list = (
    ("individual", "개인"),
    ("page", "페이지")
)

product_tag_list = (
    ('all', "전체"),
    ("it", "IT/인터넷"),
    ("food", "식품/맛집"),
    ("fashion", "패션/뷰티"),
    ("pet", "반려동물"),
    ("car", "자동차"),
    ("travel", "여행/취미"),
    ("health", "건강/의료"),
    ("interior", "인테리어"),
    ("etc", "기타"),
)
"""
("game", "게임"),
("financial", "재테크/금융"),
("study", "취업/학업"),
("baby", "육아"),
("media", "미디어/영화"),
("music", "음악"),
("diet", "다이어트"),
("life", "일상/생활"),
("picture", "사진"),
("love", "결혼/연애"),
("sports", "스포츠/레저"),
"""

class Product(models.Model):
    # 판매자 instance
    seller = models.ForeignKey(Seller, null=False, blank=False)

    # sns 선택
    sns_type = models.CharField(choices=sns_type_list, max_length=15, null=False)

    # sns 추가정보
    sns_additional_info = models.CharField(choices=sns_additional_info_list, max_length=15, null=False)

    # 성별
    sex = models.CharField(choices=(("male","남자"),("female","여자")), max_length=15, null=False)

    # 주소 공개 여부
    is_url_open = models.BooleanField(default=True)

    # sns 주소
    sns_url = models.URLField(null=True, blank=True)

    # 팔로워수
    follower_num = models.CharField(max_length=255, null=True, blank=True)

    # 일평균 방문자수
    follower_visit_num = models.CharField(max_length=255, null=True, blank=True)

    # 친구수
    follower_friends_num = models.CharField(max_length=255, null=True, blank=True)

    # 포스팅가능 분야
    product_tag = GenericRelation("ProductTag", null=True, blank=True)

    # 작업 전 유의사항
    message_to_buyer = models.TextField(null=True, blank=True)

    # 한줄소개
    oneline_intro = models.CharField(max_length=255, null=True, blank=True)

    # 상품소개
    description = summer_fields.SummernoteTextField(null=True, blank=True)

    # 가격
    price = models.PositiveIntegerField(default=0)

    # 원고가능여부
    manuscript_available = models.BooleanField(default=True)

    # 원고 추가비용
    manuscript_price = models.PositiveIntegerField(default=0)

    # 상위노출여부
    highrank_available = models.BooleanField(default=False)

    # 상위노출 추가비용
    highrank_price = models.PositiveIntegerField(default=0)

    # 작업기간
    working_period = models.PositiveIntegerField(default=0)

    # 승인 전 전달사항(관리자에게 할말)
    message_to_admin = models.TextField(null=True, blank=True)

    # 구매 만족도
    rating = models.DecimalField(default=0.00, decimal_places=2, max_digits=3)

    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    # 판매중 or 판매완료
    is_now_selling = models.BooleanField(default=True)

    objects = ProductManager()

    # 필드 업데이트 감지를 위한 트래커
    tracker = FieldTracker()

    def __unicode__(self):
        return u'%s' % (self.oneline_intro)

    @property
    def sns_type_image_url(self):
        image_url = None

        if self.sns_type == 'blog':
            image_url = '/static/img/naver.png'
        elif self.sns_type == 'facebook':
            image_url = '/static/img/facebook.png'
        elif self.sns_type == 'instagram':
            image_url = '/static/img/insta.png'
        elif self.sns_type == 'kakaostory':
            image_url = '/static/img/kakao.png'

        return image_url

    @property
    def sns_type_color(self):
        color = None

        if self.sns_type == 'blog':
            color = '#20CA24'
        elif self.sns_type == 'facebook':
            color = '#3B579D'
        elif self.sns_type == 'instagram':
            color = '#CFAE89'
        elif self.sns_type == 'kakaostory':
            color = '#FEDD43'

        return color

    @property
    def get_absolute_url(self):
        return reverse('product_detail', kwargs={"product_id": self.id})

    @property
    def get_price(self):
        return self.price


class ProductTag(models.Model):
    tag = models.CharField(choices=product_tag_list, max_length=15, null=False)
    content_type = models.ForeignKey(ContentType, related_name='ptags')
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __unicode__(self):
        return self.tag
