#-*- coding: utf-8 -*-
from django import template
from carts.models import Cart, WishList
from django.contrib.contenttypes.models import ContentType
import datetime, pytz

register = template.Library()

@register.filter(name='time_since')
def time_since(date, default="just now"):
    now = datetime.datetime.utcnow().replace(tzinfo = pytz.utc)
    diff = now - date
    periods = (
        (diff.days / 365, "년", "년"),
        (diff.days / 30, "월", "개월"),
        (diff.days / 7, "주", "주"),
        (diff.days, "일", "일"),
        (diff.seconds / 3600, "시간", "시간"),
        (diff.seconds / 60, "분", "분"),
        (diff.seconds, "", "초"),
    )
    for period, singular, plural in periods:
        if period:
            return "%d%s 전" % (period, singular if period == 1 else plural)
    return default


@register.filter(name='round_count')
def round_count(num):
    count = int(num)

    if count >= 100000 or (count >= 10000 and round(count / 10000, 1) % 10 == 0):
        result = str(int(round(count / 10000))) + '만'
    elif count >= 10000:
        result = str(int(round(count / 10000, 1))) + '만'
    elif count >= 1000:
        if round(count / 1000, 1) % 10 != 0:
            result = str(round(count / 1000, 1)) + '천'
        else:
            result = str(int(round(count / 1000))) + '천'
    else:
        result = str(count)

    return result


@register.filter(name='user_wish_count')
def user_wish_count(user_id):
    wish_count = WishList.objects.filter(
        user__id=user_id
    ).count()
    return wish_count


@register.filter(name='user_cart_count')
def user_cart_count(cart_id):
    if cart_id:
        cart = Cart.objects.get(id=cart_id)
        return cart.cartitem_set.all().count()
    else:
        return 0


@register.filter(name='multi_minus')
def multi_minus(amount):
    return amount * -1