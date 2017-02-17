# -*- coding: utf-8 -*-
import requests
import json

from django.shortcuts import render, Http404, HttpResponse
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import PointTransaction, PointHistory, Order, OrderItem, Point, Mileage
from reviews.models import ProductReview
from socialup.mixins import AjaxRequireMixin
from carts.models import Cart
from .iamport import validation_prepare
from datetime import datetime, timedelta
from markets.models import Product
from .forms import ReviewForm


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
                'detail': item.detail
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

    try:
        user_point = Point.objects.get(user=request.user)
        user_point_val = getattr(user_point, 'point')
        user_mileage = Mileage.objects.get(user=request.user)
        user_mileage_val = getattr(user_mileage, 'mileage')
    except:
        user_point_val = 0
        user_mileage_val = 0

    template = 'account/dashboard_purchase.html'
    context = {
        "order": order,
        "cart": cart_list,
        "user_point_val": user_point_val,
        "user_mileage_val": user_mileage_val
    }

    return render(request, template, context)


class CheckoutAjaxView(AjaxRequireMixin, View):
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return JsonResponse({}, status=401)

        user = request.user
        order = request.POST.get('order')
        mileage = request.POST.get('mileage')
        point = request.POST.get('point')
        type = request.POST.get('type')

        try:
            trans = Order.objects.get(
                user=user,
                order_id=order
            )

            trans.mileage = mileage
            trans.point = point
            trans.type = type
            trans.save()
        except:
            trans = None

        if trans is not None:
            pay_total = int(trans.order_total) - int(trans.point) - int(trans.mileage)
            if pay_total > 0:

                # 아임포트 결제 사전 검증 단계
                validation_prepare(order, pay_total)

                data = {
                    "works": True,
                    "total": pay_total
                }
                return JsonResponse(data)

            # 0원 결제
            elif pay_total == 0 and type == 'point':
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
    if request.POST.get('is_status_change'):
        order_item_id = request.POST.get('order_item')
        try:
            order_item = OrderItem.objects.get(id=order_item_id)
            new_status = request.POST.get('new_status')
            if order_item.status == 'paid' and new_status == 'request_refund' or \
            order_item.status != 'request_refund' and new_status == 'finished' or \
            order_item.status != 'refunded' and new_status == 'finished' :
                order_item.status = new_status
                order_item.save()
        except:
            pass

    if request.POST.get('repurchase'):
        order_item_id = request.POST.get('order_item')
        try:
            order_item = OrderItem.objects.get(id=order_item_id)
        except:
            pass
        if order_item is not None:
            new_cart = Cart.objects.create(user=request.user)
            request.session['cart_id'] = new_cart.id

            new_cart_item = order_item.cart_item
            new_cart_item.pk = None
            new_cart_item.cart = new_cart
            new_cart_item.save()

            data = {
                "cart_id": new_cart.id,
                "status": "success",
            }

            if data is not None:
                return HttpResponse(json.dumps(data), content_type='application/json')
            else:
                raise Http404

    if request.POST.get('transaction_details'):
        order_item_id = request.POST.get('order_item_id')
        order_item = OrderItem.objects.get(id=order_item_id)
        template='account/transaction_details.html'
        context={
            "order_item": order_item,
        }
        return render(request, template, context)

    if request.POST.get('is_review_upload'):
        order_item = OrderItem.objects.get(id=request.POST.get('order_item_id'))
        product = order_item.cart_item.item
        review, review_created = ProductReview.objects.get_or_create(order_item=order_item, product=product, user=request.user)
        review_form = ReviewForm(request.POST, instance=review)
        if review_form.is_valid():
            review_form.save(commit=True)

    order_items = OrderItem.objects.filter(user=request.user)
    order_items_ready = order_items.filter(user=request.user, status='paid')
    order_items_processing = order_items.filter(user=request.user, status='processing')
    order_items_wait_confirm = order_items.filter(user=request.user, status='wait_confirm')
    order_items_finished = order_items.filter(user=request.user, status='finished')
    order_items_refunded = order_items.filter(user=request.user, status='refunded')
    order_items_request_refund = order_items.filter(user=request.user, status='request_refund')

    # 주석 처리된 부분은 review_forms를 던져서 유저가 이전에 작성했던 리뷰들을 볼 수 있게 하기 위함임
    # 현재는 이미 서비스 평가했던걸 다시 평가하면 빈 폼이 뜨지만 제출하면 수정되도록 해둠
    review_form = ReviewForm()
    review_forms = {}
    for order_item in order_items:
        try:
            review = ProductReview.objects.get(order_item=order_item)
            review_form = ReviewForm(instance=review)
        except:
            review_form = ReviewForm()
        review_forms[order_item.id] = review_form

    template = 'account/dashboard_purchase_list.html'
    context = {
        "order_items": order_items,
        "order_items_ready": order_items_ready,
        "order_items_processing": order_items_processing,
        "order_items_wait_confirm": order_items_wait_confirm,
        "order_items_finished": order_items_finished,
        "order_items_refunded": order_items_refunded,
        "order_items_request_refund": order_items_request_refund,
        "order_items_request_refund_length": order_items_request_refund.count(),
        "review_form": review_form,
        "review_forms": review_forms,
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
    if request.POST.get('order_id'):
        order_id = request.POST.get('order_id')
        try:
            order = Order.objects.get(order_id=order_id)
            order.delete()
        except:
            pass
    context = {

    }

    return render(request, template, context)