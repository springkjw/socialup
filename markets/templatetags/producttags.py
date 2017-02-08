#-*- coding: utf-8 -*-
from django import template
from carts.models import Cart, WishList, CartItem
from billing.models import Order
from accounts.models import MyUser
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

@register.filter(name='user_purchase_count')
def user_purchase_count(user_id):
    order_list = Order.objects.filter(user__id=user_id, status='paid')
    purchase_count = 0
    for order in order_list:
        temp_cart = Cart.objects.filter(id=order.cart_id)
        cart_items = CartItem.objects.filter(cart=temp_cart[0])
        purchase_count += len(cart_items)

    return purchase_count

@register.filter(name='multi_minus')
def multi_minus(amount):
    return amount * -1


# @register.simple_tag 를 쓰려 했으나 작동 안되어서 @register.filter 장식자를 붙이고 불필요한 user_id 파라메터를 받고 세개의 메소드로 나눠서 작성. 작동엔 문제없지만 수정되면 좋겠음.
# 고객센터, 1:1 문의 부분. 메세지 받을 계정이 바뀌면 email부분을 수정하면 됨.
@register.filter(name='cs_admin_user_id')
def cs_admin_user_id(user_id):
    try:
        cs_admin_user = MyUser.objects.get(email='social_up@naver.com')
        cs_admin_user_id = cs_admin_user.id
    except:
        cs_admin_user_id = None
    return cs_admin_user_id


@register.filter(name='cs_admin_user_short_name')
def cs_admin_user_short_name(user_id):
    try:
        cs_admin_user = MyUser.objects.get(email='social_up@naver.com')
        cs_admin_user_short_name = cs_admin_user.get_short_name()
    except:
        cs_admin_user_short_name = None
    return cs_admin_user_short_name


@register.filter(name='cs_admin_user_avatar')
def cs_admin_user_avatar(user_id):
    try:
        cs_admin_user = MyUser.objects.get(email='social_up@naver.com')
        cs_admin_user_avatar = cs_admin_user.get_avatar()
    except:
        cs_admin_user_avatar = None
    return cs_admin_user_avatar
