# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, HttpResponse, Http404
from django.views.generic.base import View
from django.views.generic.detail import SingleObjectMixin
from django.core.urlresolvers import reverse
from .models import Cart, CartItem, WishList
from markets.models import Product

import json


class CartView(SingleObjectMixin, View):
    model = Cart
    template_name = 'account/dashboard_cart.html'

    def get_object(self, *args, **kwargs):
        self.request.session.set_expiry(6000)
        cart_id = self.request.session.get('cart_id')

        if cart_id is None:
            cart = Cart()
            cart.save()
            cart_id = cart.id
            self.request.session["cart_id"] = cart_id

        try:
            cart = Cart.objects.get(id=cart_id)

            if self.request.user.is_authenticated():
                cart.user = self.request.user
                cart.save()
        except:
            del self.request.session['cart_id']
            cart = None

        if cart is not None:
            product_list = []
            cart_list = []

            cart_item = cart.cartitem_set.all()
            for i in cart_item:
                product_list.append(i.item.product.id)
            product_list = list(set(product_list))

            for product in product_list:
                c_list = []
                for c in cart.cartitem_set.all():
                    if product == c.item.product.id:
                        c_list.append(c)
                cart_list.append(c_list)
        else:
            cart_list = []

        result = {
            "cart": cart,
            "item": cart_list
        }

        return result

    def get(self, request, *args, **kwargs):
        cart = self.get_object()['cart']
        item_id = request.GET.get("item")
        product_id = request.GET.get("product_item")
        buy_id = request.GET.get("buy_item")
        delete_item = request.GET.get("delete")

        if item_id:
            item_instance = get_object_or_404(Product, id=item_id)
            cart_item = CartItem.objects.get_or_create(cart=cart, item=item_instance)[0]
            if delete_item:
                if not item_instance.is_default:
                    cart_item.delete()
            else:
                cart_item.save()

        if buy_id:
            # product 기본가 variation 추가
            buy_instance = get_object_or_404(Product, id=buy_id)

            # cart session 초기화
            del request.session['cart_id']

            # cart 생성
            cart = self.get_object()['cart']

            cart_item = CartItem.objects.get_or_create(cart=cart, item=buy_instance)[0]
            cart_item.save()

            return HttpResponseRedirect(reverse('purchase', kwargs={'cart_id': self.request.session.get('cart_id')}))

        if product_id:
            product_item = CartItem.objects.filter(item__product__id=product_id)
            if delete_item:
                product_item.delete()

        context = {
            "object": self.get_object()
        }
        template = self.template_name
        return render(request, template, context)

    # 카트에서 바로 구매 클릭 시
    def post(self, request, *args, **kwargs):
        option = request.POST.getlist('cart[]')
        default = Product.objects.get(id=option[0])

        if option:
            del request.session['cart_id']

            cart = add_to_cart(request, default, option)

            if cart is not None:
                data = {
                    "status": "success",
                    "cart_id": cart.id
                }

                return HttpResponse(json.dumps(data), content_type='application/json')
            else:
                raise Http404


class WishListView(SingleObjectMixin, View):
    model = WishList
    template_name = 'account/dashboard_wishlist.html'

    def get_object(self, *args, **kwargs):
        if self.request.user.is_authenticated():
            user = self.request.user
            try:
                wish_list = WishList.objects.filter(user=user)
            except:
                wish_list = None
            return wish_list
        else:
            return HttpResponseRedirect('/login/')

    def get(self, request, *args, **kwargs):
        user = request.user
        product_id = request.GET.get("product")
        delete_item = request.GET.get("delete")

        if product_id and user:
            product_instance = get_object_or_404(Product, id=product_id)
            wish_item = WishList.objects.get_or_create(user=user, item=product_instance)[0]
            if delete_item:
                wish_item.delete()
            else:
                wish_item.save()
        context = {
            "lists": self.get_object()
        }
        template = self.template_name
        return render(request, template, context)


def add_to_cart(request, default, list):
    data = {
        "status": "fail",
        "cart_id": None
    }
    # request 세션 100분 설정
    request.session.set_expiry(6000)
    # card_id를 세션에서 가져오기
    cart_id = request.session.get('cart_id')

    # try:
    #     cart = Cart.objects.get(id=cart_id, user=request.user)
    #
    # except Cart.DoesNotExist:
    #     cart = Cart()
    #     cart.save()
    #     cart_id = cart.id
    #     request.session["cart_id"] = cart_id
    #
    # # 세션 카트 id 바탕으로 카트 오브젝트 조회
    # try:
    #     cart_instance = Cart.objects.get(id=cart_id)
    #
    #     if request.user.is_authenticated():
    #         cart_instance.user = request.user
    #         cart_instance.save()
    # except:
    #     del request.session['cart_id']
    #     cart_instance = None

    cart = Cart.objects.filter(id=cart_id, user=request.user)
    if cart.exists():
        cart_instance = cart[0]
    else:
        cart_instance = Cart.objects.create(user=request.user)
        request.session['cart_id'] = cart_instance.id

    # 카트 인스턴스가 존재할 때
    if cart_instance is not None:
        # ajax로 넘어온 variation item 조회
        for item in list:
            # variation item이 존재할 때
            if Product.objects.filter(id=item).exists():
                option_instance = Product.objects.get(id=item)
                cart_item, created = CartItem.objects.get_or_create(cart=cart_instance, item=option_instance)
                if created:
                    data = {
                        "status": "success",
                        "cart_id": cart.id,
                    }
                cart_item.save()
            # 없으면 카트 인스턴스 초기화
            else:
                cart_instance = None
    return cart_instance
