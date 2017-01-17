# -*- coding: utf-8 -*-
import requests
import json

from django.shortcuts import render, Http404
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import PointTransaction, PointHistory, Order
from socialup.mixins import AjaxRequireMixin
from carts.models import Cart
from .iamport import validation_prepare
from datetime import datetime, timedelta
from markets.models import Product

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


@login_required
def charge_point(request):
    template = 'account/dashboard_charge.html'

    if request.is_ajax():
        name = request.GET.get('name')
        phone = request.GET.get('phone')

        try:
            user = request.user
        except:
            raise Http404

        if not user.name and name is not None:
            user.name = name
            user.save()

        if not user.phone and phone is not None:
            user.phone = phone
            user.save()

    context = {
    }
    return render(request, template, context)


@login_required
def history_point(request):
    delta = request.GET.get('delta')
    if delta is None:
        delta = 30

    last_month = datetime.today() - timedelta(days=int(delta))
    obj = PointHistory.objects.filter(user=request.user, timestamp__gte=last_month)

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
                'product': item,
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


@login_required
def purchase(request, cart_id):
    # 판매자 정보 확인 및 저장
    if request.is_ajax():
        name = request.GET.get('name')
        phone = request.GET.get('phone')

        try:
            user = request.user
        except:
            raise Http404

        if not user.name and name is not None:
            user.name = name
            user.save()

        if not user.phone and phone is not None:
            user.phone = phone
            user.save()

    cart = Cart.objects.get(user=request.user, id=cart_id)

    if cart is not None:
        product_list = []
        cart_list = []

        cart_item = cart.cartitem_set.all()
        for i in cart_item:
            product_list.append(i.item.id)
        product_list = list(set(product_list))

        for product in product_list:
            c_list = []
            c_price = 0
            for c in cart.cartitem_set.all():
                if product == c.item.id:
                    c_list.append(c)
                    c_price += c.item.price
            c_data = {
                "item": c_list,
                "price": c_price
            }
            cart_list.append(c_data)

    seller = cart.items.all()[0].seller

    order, created = Order.objects.get_or_create(
        user=request.user,
        cart=cart,
        seller=seller,
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
                trans.delete()
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


@login_required
def purchase_list(request):
    orders = Order.objects.filter(user=request.user).exclude(status='created')
    orders_wait = Order.objects.filter(user=request.user, status='paid')
    orders_processing = Order.objects.filter(user=request.user, status='processing')
    status_0 = orders.filter(status='paid').count()
    status_1 = orders.filter(status='processing').count()
    status_2 = orders.filter(status='finished').count()
    status_3 = orders.filter(status='refunded').count()

    template = 'account/dashboard_purchase_list.html'
    context = {
        "orders": orders,
        "order_wait":orders_wait,
        "order_processing": orders_processing,
        "status_0": status_0,
        "status_1": status_1,
        "status_2": status_2,
        "status_3": status_3,
    }

    return render(request, template, context)


@login_required
def charge_success(request):
    template = 'charge/charge_success.html'
    context = {

    }

    return render(request, template, context)


@login_required
def charge_fail(request):
    template = 'charge/charge_fail.html'
    context = {

    }

    return render(request, template, context)

@login_required
def pay_success(request):
    template = 'account/dashboard_success.html'
    del request.session['cart_id']
    context = {

    }

    return render(request, template, context)

@login_required
def pay_fail(request):
    template = 'account/dashboard_fail.html'
    context = {

    }

    return render(request, template, context)