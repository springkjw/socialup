#-*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType

from markets.models import Product

sns_type = (
    ("blog", "블로그"),
    ("facebook", "페이스북"),
    ("instagram", "인스타그램"),
    ("kakaostroy", "카카오스토리"),
    ("cafe", "카페"),
    ("twitter", "트위터"),
    ("pola", "폴라"),
    ("afreeca", "아프리카TV"),
    ("etc", "기타"),
)


class SocialAnalytics(models.Model):
    analytics = models.CharField(max_length=20, null=False, blank=True)
    outcome = models.PositiveIntegerField(default=0)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    def __unicode__(self):
        return self.analytics


class Sns(models.Model):
    product = models.ForeignKey(Product, null=True, blank=True)
    type = models.CharField(max_length=30, choices=sns_type)
    url = models.URLField(null=True, blank=True)
    is_confirm = models.BooleanField(default=False)
    analytics = GenericRelation("SocialAnalytics", null=True, blank=True)

    def __unicode__(self):
        return self.type