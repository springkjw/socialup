# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.db.models.signals import post_save
from markets.models import Product
from accounts.models import MyUser, Seller
from billing.models import OrderItem, Mileage, MileageHistory

SATISFY_CHOICES = (
    ('good','만족'),
    ('neutral','보통'),
    ('bad','불만족'),
)

class ProductReview(models.Model):
    product = models.ForeignKey(Product)
    order_item = models.ForeignKey(OrderItem)
    user = models.ForeignKey(MyUser)
    review = models.TextField(null=True, blank=True)
    rating = models.DecimalField(default=0.00, decimal_places=2, max_digits=3)
    contents_satisfy = models.CharField(max_length=10, choices=SATISFY_CHOICES, default='good')
    ad_satisfy = models.CharField(max_length=10, choices=SATISFY_CHOICES, default='good')
    kind_satisfy = models.CharField(max_length=10, choices=SATISFY_CHOICES, default='good')
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)


    def __unicode__(self):
        return str(self.rating)


def new_review_receiver(sender, instance, created, *args, **kwargs):
    # 서비스 평가시 0.5% 적립
    if created:
        try:
            mileage = Mileage.objects.get(user=instance.user)
            amount = int(instance.order_item.cart_item.line_item_total / 200)
            mileage.mileage += amount
            mileage.save()
            mileage_history = MileageHistory.objects.create(user=instance.user,
                                                            amount=amount,
                                                            detail=instance.order_item.cart_item.item.oneline_intro+" 서비스평가"
                                                            )
        except:
            pass

    # product rating 업데이트
    product = Product.objects.get(id=instance.product.id)
    product_reviews = ProductReview.objects.filter(product=product)
    sum_of_ratings = 0
    for review in product_reviews:
        sum_of_ratings += review.rating

    avg_of_rating = sum_of_ratings / len(product_reviews)
    product.rating = avg_of_rating
    product.save()

    # seller rating 업데이트
    seller = Seller.objects.get(id=product.seller.id)
    products = Product.objects.filter(seller=seller)
    sum_of_seller_ratings = 0
    num_seller_reviews = 0
    for each_product in products:
        each_product_reviews = ProductReview.objects.filter(product=each_product)
        for each_product_review in each_product_reviews:
            sum_of_seller_ratings += each_product_review.rating
        num_seller_reviews += each_product.get_num_reviews

    if num_seller_reviews :
        avg_of_seller_rating = sum_of_seller_ratings / num_seller_reviews
    else :
        avg_of_seller_rating = 0
    seller.rating = avg_of_seller_rating
    seller.save()


post_save.connect(new_review_receiver, sender=ProductReview)
