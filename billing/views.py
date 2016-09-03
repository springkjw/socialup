# -*- coding: utf-8 -*-
import requests
import json

from django.shortcuts import render, Http404
from django.views.generic import View
from django.conf import settings
from django.http import JsonResponse
from .models import PointTransaction, PointHistory, Order
from socialup.mixins import AjaxRequireMixin
from carts.models import Cart
from .iamport import validation_prepare


class PointCheckoutAjaxView(AjaxRequireMixin, View):
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return JsonResponse({}, status=401)

        user = request.user
        amount = request.POST.get('amount')
        type = request.POST.get('type')

        try:
            trans = PointTransaction.objects.create_new(
                user=user,
                amount=amount,
                type=type
            )
        except:
            trans = None

        if trans is not None:
            data = {
                "works": True,
                "merchant_id": trans
            }
            return JsonResponse(data)
        else:
            return JsonResponse({}, status=401)


class PointImpAjaxView(AjaxRequireMixin, View):
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return JsonResponse({}, status=401)

        user = request.user
        merchant_id = request.POST.get('merchant_id')
        imp_id = request.POST.get('imp_id')
        amount = request.POST.get('amount')

        try:
            trans = PointTransaction.objects.get(
                user=user,
                order_id=merchant_id,
                amount=amount
            )
        except:
            trans = None

        if trans is not None:
            trans.transaction_id = imp_id
            trans.success = True
            trans.save()

            data = {
                "works": True
            }

            return JsonResponse(data)
        else:
            return JsonResponse({}, status=401)


def charge_point(request):
    template = 'account/dashboard_charge.html'
    context = {
    }
    return render(request, template, context)


def history_point(request):
    obj = PointHistory.objects.filter(user=request.user)

    result = []
    result_charge = []
    result_usage = []
    for item in obj:
        data = {
            'timestamp': item.timestamp,
            'type': switch_history_type(item.type),
            'amount': item.amount,
            'status': switch_history_status(item.status),
            'receipt': item.receipt
        }
        result.append(data)

        if item.amount > 0:
            data_charge = {
                'timestamp': item.timestamp,
                'type': switch_history_type(item.type),
                'amount': item.amount,
                'status': switch_history_status(item.status),
                'receipt': item.receipt
            }
            result_charge.append(data_charge)
        else:
            data_usage = {
                'timestamp': item.timestamp,
                'product': item.product,
                'amount': item.amount,
                'status': switch_history_status(item.status),
            }
            result_usage.append(data_usage)

    template = 'account/dashboard_point_history.html'
    context = {
        "history": result,
        "history_charge": result_charge,
        "history_usage": result_usage
    }

    return render(request, template, context)


def switch_history_type(type):
    return {
        'card': '신용카드',
        'phone': '휴대폰결제'
    }.get(type, '알수없음')


def switch_history_status(status):
    return {
        'paid': '결제완료'
    }.get(status, '알수없음')


def purchase(request, cart_id):
    cart = Cart.objects.get(user=request.user, id=cart_id)

    if cart is not None:
        product_list = []
        cart_list = []

        cart_item = cart.cartitem_set.all()
        for i in cart_item:
            product_list.append(i.item.product.id)
        product_list = list(set(product_list))

        for product in product_list:
            c_list = []
            c_price = 0
            for c in cart.cartitem_set.all():
                if product == c.item.product.id:
                    c_list.append(c)
                    c_price += c.item.price
            c_data = {
                "item": c_list,
                "price": c_price
            }
            cart_list.append(c_data)

    order, created = Order.objects.get_or_create(
        user=request.user,
        cart=cart,
        order_total=cart.subtotal
    )

    template = 'account/dashboard_purchase.html'
    context = {
        "order": order,
        "cart": cart_list
    }

    return render(request, template, context)


class CheckoutAjaxView(AjaxRequireMixin, View):
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return JsonResponse({}, status=401)

        user = request.user
        order = request.POST.get('order')
        point = request.POST.get('point')
        type = request.POST.get('type')

        try:
            trans = Order.objects.get(
                user=user,
                order_id=order
            )

            trans.point = point
            trans.type = type
            trans.save()
        except:
            trans = None

        if trans is not None:
            pay_total = int(trans.order_total) - int(trans.point)

            if not pay_total < 0:

                # 아임포트 결제 사전 검증 단계
                validation_prepare(order, pay_total)

                data = {
                    "works": True,
                    "total": pay_total
                }
                return JsonResponse(data)
            else:
                return JsonResponse({}, status=401)
        else:
            return JsonResponse({}, status=401)


class ImpAjaxView(AjaxRequireMixin, View):
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return JsonResponse({}, status=401)

        user = request.user
        merchant_id = request.POST.get('merchant_id')
        imp_id = request.POST.get('imp_id')
        amount = request.POST.get('amount')

        try:
            trans = Order.objects.get(
                user=user,
                order_id=merchant_id,
            )


        except:
            trans = None

        if trans is not None:
            trans.transaction_id = imp_id
            trans.success = True
            trans.save()

            data = {
                "works": True
            }

            return JsonResponse(data)
        else:
            return JsonResponse({}, status=401)


def purchase_list(request):
    # if request.is_ajax():
    #     user_id = request.GET.get('user_id')
    #
    #     url = 'https://api.sendbird.com/v3/group_channels'
    #     headers = {
    #         "Api-Token": settings.SD_API_TOKEN
    #     }
    #     data = {
    #         # "name": string,
    #         # "cover_url": string,
    #         # "data": string,
    #         "user_ids": [user_id],
    #         "is_distinct": True
    #     }
    #
    #     req = requests.post(url, data=json.dumps(data), headers=headers)
    #
    #     res = json.loads(req.content)
    #
    #     channel_url = res['channel_url']
    #
    #     if channel_url:
    #         # url_m = 'https://api.sendbird.com/v3/group_channels/%s/messages' % (channel_url)
    #         # data_m = {
    #         #     "message_ts": "10"
    #         # }
    #         # req_m = requests.get(url_m, params=data_m, headers=headers)
    #         # res_m = json.loads(req_m.content)
    #
    #         return JsonResponse(res_m)

    purchase_list = Order.objects.filter(user=request.user)

    template = 'account/dashboard_purchase_list.html'
    context = {
        "list": purchase_list
    }

    return render(request, template, context)
