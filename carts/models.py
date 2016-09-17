from __future__ import unicode_literals

from django.db import models
from django.db.models.signals import pre_save, post_save, post_delete
from accounts.models import MyUser
from markets.models import Product, Variation


class CartItem(models.Model):
    cart = models.ForeignKey("Cart")
    item = models.ForeignKey(Variation)
    quantity = models.PositiveIntegerField(default=1)
    line_item_total = models.IntegerField(default=0)

    def __unicode__(self):
        return self.item.title

    def remove(self):
        return self.item.remove_from_cart()


def cart_item_pre_save_receiver(sender, instance, *args, **kwargs):
    qty = instance.quantity
    if qty >= 1:
        price = instance.item.get_price
        line_item_total = price * qty
        instance.line_item_total = line_item_total


pre_save.connect(cart_item_pre_save_receiver, sender=CartItem)


def cart_item_post_save_receiver(sender, instance, *args, **kwargs):
    instance.cart.update_subtotal()


post_save.connect(cart_item_post_save_receiver, sender=CartItem)
post_delete.connect(cart_item_post_save_receiver, sender=CartItem)


class Cart(models.Model):
    user = models.ForeignKey(MyUser, null=True, blank=True)
    items = models.ManyToManyField(Variation, through=CartItem)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    subtotal = models.IntegerField(default=0)

    def __unicode__(self):
        return str(self.id)

    def update_subtotal(self):
        subtotal = 0
        items = self.cartitem_set.all()
        for item in items:
            subtotal += item.line_item_total
        self.subtotal = subtotal
        self.save()


class WishList(models.Model):
    user = models.ForeignKey(MyUser)
    item = models.ForeignKey(Product)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __unicode__(self):
        return self.item.title
