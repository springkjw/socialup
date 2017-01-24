# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# python import
import time
import random
import hashlib

# django import
from django.db import models
from django.db.models.signals import post_save

# app import
from accounts.models import MyUser, Seller
from markets.models import Product
from carts.models import Cart, CartItem
from .iamport import validation_prepare, get_transaction

class Mileage(models.Model):
    user = models.OneToOneField(MyUser)
    mileage = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    timestamp = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __unicode__(self):
        return str(self.mileage)


class MileageHistory(models.Model):
    user = models.ForeignKey(MyUser)
    amount = models.IntegerField(default=0)
    detail = models.CharField(max_length=255, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return str(self.amount)


class Point(models.Model):
    user = models.OneToOneField(MyUser)
    point = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    timestamp = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __unicode__(self):
        return str(self.point)


class PointHistory(models.Model):
    user = models.ForeignKey(MyUser)
    amount = models.IntegerField(default=0)
    type = models.CharField(max_length=20, null=True, blank=True)
    detail = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=20, null=True, blank=True)
    receipt = models.CharField(max_length=255, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return str(self.amount)


def new_user_receiver(sender, instance, created, *args, **kwargs):
    if created:
        user = MyUser.objects.get(id=instance.id)
        if not user.is_admin:
            point = Point(
                user=instance
            )
            point.save()

            mileage = Mileage(
                user=instance
            )
            mileage.save()

post_save.connect(new_user_receiver, sender=MyUser)


class PointTransactionManager(models.Manager):
    # 새로운 트랜젝션 생성
    def create_new(self, user, amount, type, success=None, transaction_status=None):
        if not user:
            raise ValueError("유저가 확인되지 않습니다.")
        short_hash = hashlib.sha1(str(random.random())).hexdigest()[:2]
        time_hash = hashlib.sha1(str(int(time.time()))).hexdigest()[-3:]
        base = str(user.email).split("@")[0]
        key = hashlib.sha1(short_hash + time_hash + base).hexdigest()[:10]
        new_order_id = "%s" % (key)

        # 아임포트 결제 사전 검증 단계
        validation_prepare(new_order_id, amount)

        # 트랜젝션 저장
        new_trans = self.model(
            user=user,
            order_id=new_order_id,
            amount=amount,
            type=type
        )

        if success is not None:
            new_trans.success = success
            new_trans.transaction_status = transaction_status

        new_trans.save(using=self._db)
        return new_trans.order_id

    # 생선된 트랜잭션 검증
    def validation_trans(self, merchant_id):
        result = get_transaction(merchant_id)

        if result['status'] is not 'paid':
            return result
        else:
            return None

    def all_for_user(self, user):
        return super(PointTransactionManager, self).filter(user=user)

    def get_recent_user(self, user, num):
        return super(PointTransactionManager, self).filter(user=user)[:num]


class PointTransaction(models.Model):
    user = models.ForeignKey(MyUser)
    transaction_id = models.CharField(max_length=120, null=True, blank=True)
    order_id = models.CharField(max_length=120, unique=True)
    amount = models.PositiveIntegerField(default=0)
    success = models.BooleanField(default=False)
    transaction_status = models.CharField(max_length=220, null=True, blank=True)  # if fail
    type = models.CharField(max_length=120)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)

    objects = PointTransactionManager()

    def __unicode__(self):
        return self.order_id

    class Meta:
        ordering = ['-created']


def new_point_trans_validation(sender, instance, created, *args, **kwargs):
    if instance.transaction_id:
        # 거래 후 아임포트에서 넘긴 결과
        v_trans = PointTransaction.objects.validation_trans(
            merchant_id=instance.order_id
        )

        res_merchant_id = v_trans['merchant_id']
        res_imp_id = v_trans['imp_id']
        res_amount = v_trans['amount']

        # 데이터베이스에 실제 결제된 정보가 있는지 체크
        r_trans = PointTransaction.objects.filter(
            order_id=res_merchant_id,
            transaction_id=res_imp_id,
            amount=res_amount
        ).exists()

        if not v_trans or not r_trans:
            raise ValueError('비정상적인 거래입니다.')
        else:
            try:
                # 유저 포인트 추가
                p = Point.objects.get(user=instance.user)
                point = p.point
                # 결제 금액의 90%만 충전(부가세 고려)
                new_point = point + int(round(v_trans['amount'] / 1.1))
                p.point = new_point
                p.save()
            except:
                raise ValueError('포인트 적립에 문제가 발생했습니다.')

            try:
                # 포인트 history 추가
                h = PointHistory(
                    user=instance.user,
                    amount=int(round(v_trans['amount'] / 1.1)),
                    type=v_trans['type'],
                    status=v_trans['status'],
                    receipt=v_trans['receipt_url']
                )
                h.save()
            except:
                raise ValueError('포인트 적립에 문제가 발생했습니다.')


post_save.connect(new_point_trans_validation, sender=PointTransaction)

ORDER_STATUS_CHOICES = (
    ('created', 'Created'),
    ('paid', 'Paid'),
    ('refunded', 'Refunded'),
    ('processing', 'Processing'),
    ('request_refund','request_refund'),
    ('wait_confirm','wait_confirm'),
    ('finished', 'Finished'),
)


class OrderManager(models.Manager):
    # 생선된 트랜잭션 검증
    def validation_trans(self, merchant_id):
        result = get_transaction(merchant_id)

        if result['status'] is not 'paid':
            return result
        else:
            return None


class Order(models.Model):
    status = models.CharField(max_length=120, choices=ORDER_STATUS_CHOICES, default='created')
    cart = models.ForeignKey(Cart, null=True)
    user = models.ForeignKey(MyUser, null=True)
    seller = models.ForeignKey(Seller, null=True)
    order_total = models.PositiveIntegerField(default=0)
    point = models.PositiveIntegerField(default=0)
    mileage = models.PositiveIntegerField(default=0)
    order_id = models.CharField(max_length=120, unique=True)
    transaction_id = models.CharField(max_length=120, null=True, blank=True)
    type = models.CharField(max_length=120, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False, null=True, blank=True)
    receipt = models.CharField(max_length=255, null=True, blank=True)

    objects = OrderManager()

    def __unicode__(self):
        return self.order_id

    def get_total_day(self):
        products = self.cart.items.all()
        total_days = 0

        for item in products:
            total_days += item.working_period

        return total_days


    class Meta:
        ordering = ['-id']


def new_order_receiver(sender, instance, created, *args, **kwargs):
    if created:
        short_hash = hashlib.sha1(str(random.random())).hexdigest()[:2]
        time_hash = hashlib.sha1(str(int(time.time()))).hexdigest()[-3:]
        base = str(instance.user.email).split("@")[0]
        key = hashlib.sha1(short_hash + time_hash + base).hexdigest()[:10]
        new_order_id = "%s" % (key)

        instance.order_id = new_order_id
        instance.save()
    else:
        if instance.transaction_id and instance.status == 'created':
            # 거래 후 아임포트에서 넘긴 결과
            v_trans = Order.objects.validation_trans(
                merchant_id=instance.order_id
            )

            res_merchant_id = v_trans['merchant_id']
            res_imp_id = v_trans['imp_id']
            res_amount = int(v_trans['amount']) + int(instance.point)

            # 데이터베이스에 실제 결제된 정보가 있는지 체크
            r_trans = Order.objects.filter(
                order_id=res_merchant_id,
                transaction_id=res_imp_id,
                order_total=res_amount
            ).exists()

            if not v_trans or not r_trans:
                raise ValueError('비정상적인 거래입니다.')
            else:
                try:
                    # 유저 포인트 감소
                    p = Point.objects.get(user=instance.user)
                    point = p.point
                    # 결제 금액의 90%만 충전(부가세 고려)
                    new_point = point - int(instance.point)
                    p.point = new_point
                    p.save()
                except:
                    raise ValueError('거래에 문제가 발생했습니다.')

                if instance.point > 0:
                    try:
                        cart_items = CartItem.objects.filter(cart=instance.cart)
                        if len(cart_items) == 1 :
                            detail = cart_items[0].item.oneline_intro
                        else:
                            detail = cart_items[0].item.oneline_intro + " 외 " + str(len(cart_items)-1) + "개"

                        # 포인트 history 추가
                        h = PointHistory(
                            user=instance.user,
                            amount=-int(instance.point),
                            status=v_trans['status'],
                            detail=detail
                        )
                        h.save()
                    except:
                        raise ValueError('거래에 문제가 발생했습니다.')

                for cart_item in CartItem.objects.filter(cart = instance.cart):
                    new_order_item = OrderItem.objects.create(user=instance.user, order=instance, cart_item=cart_item, status="paid")
                    new_order_item.save()

                instance.receipt = v_trans['receipt_url']
                instance.status = 'paid'
                instance.save()



post_save.connect(new_order_receiver, sender=Order)


PRODUCT_STATUS_CHOICES = (
    ('ready', 'Ready'),
    ('progress', 'Progress'),
    ('complete', 'Complete'),
    ('finish', 'Finish'),
    ('cancel', 'Cancel'),
)


class ProductList(models.Model):
    product = models.ForeignKey('ProductManage')
    item = models.ForeignKey(Product)

    def __unicode__(self):
        return self.item.title


class ProductManage(models.Model):
    seller = models.ForeignKey(Seller)
    customer = models.ForeignKey(MyUser)
    product = models.ForeignKey(Product, null=True, blank=True)
    items = models.ManyToManyField(ProductList)
    status = models.CharField(max_length=120, choices=PRODUCT_STATUS_CHOICES, default='ready')
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    created = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __unicode__(self):
        return self.id

    def status_in_korean(self):
        statuses = {'ready': '작업대기',
                   'progress': '작업진행',
                   'complete': '작업완료',
                   'finish': '거래완료',
                   'cancel': '취소'}
        return statuses[self.status]


def product_receiver(instance, sender, created, *args, **kwargs):
    if instance.status == 'finish':
        pass


post_save.connect(product_receiver, sender=ProductManage)

class OrderItem(models.Model):
    user = models.ForeignKey(MyUser, null=True)
    order = models.ForeignKey(Order)
    cart_item = models.ForeignKey(CartItem)
    status = models.CharField(max_length=120, choices=ORDER_STATUS_CHOICES, default='created')

    def __unicode__(self):
        return str(self.id)