from __future__ import unicode_literals

from django.db import models
from django.db.models.signals import post_save
from markets.models import Product
from accounts.models import MyUser


class ProductReview(models.Model):
    product = models.ForeignKey(Product)
    user = models.ForeignKey(MyUser)
    review = models.TextField(null=True, blank=True)
    rating = models.DecimalField(default=0.00, decimal_places=2, max_digits=3)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)


    def __unicode__(self):
        return str(self.rating)


def new_review_receiver(sender, instance, created, *args, **kwargs):
    if created:
        product = Product.objects.get(id=instance.product.id)
        ratings = ProductReview.objects.filter(product=product)
        sum_of_ratings = 0
        for rat in ratings:
            sum_of_ratings += rat.rating

        avg_of_rating = sum_of_ratings / len(ratings)

        # rating = product.rating
        # rating = (rating + instance.rating) / 2

        product.rating = avg_of_rating
        product.save()

post_save.connect(new_review_receiver, sender=ProductReview)