# -*- coding: utf-8 -*-
from django.shortcuts import (
    render,
    HttpResponse,
    Http404,
    HttpResponseRedirect,
    get_object_or_404,
    redirect,
)
from django.db.models import Sum
from django.contrib import messages
from django.forms import inlineformset_factory
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.forms import generic_inlineformset_factory
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from .models import (
    Product,
    ProductTag,
)
from .forms import ProductForm, TagForm, SellerAccountForm
from carts.models import WishList, CartItem
from carts.views import add_to_cart
from billing.models import Order, ProductManage, OrderItem
from accounts.models import MyUser, Seller, Profit, SellerAccount, Withdrawal
from accounts.forms import WithdrawalForm
from reviews.models import ProductReview
from billing.models import OrderItem


from django.core import serializers

import json


@login_required
def product_detail(request, product_id):
    # product_id로 상품 조회
    product_instance = Product.objects.active()
    product = get_object_or_404(product_instance, id=product_id)
    product_tag = ProductTag.objects.filter(object_id=product.id, content_type=ContentType.objects.get_for_model(product))

    # product 판매자
    seller = product.seller
    # product 판매자 평점 조회
    seller_rating = int(round(seller.rating * 20))
    seller_count = Product.objects.filter(seller=seller).count()

    reviews = ProductReview.objects.filter(product=product)
    reviews_count = reviews.count()
    # 현재 product가 담긴 현재 유저의 찜목록
    is_user_wished = False
    user_wished_list = WishList.objects.filter(user=request.user, item=product.id)
    if user_wished_list:
        is_user_wished = True

    if request.is_ajax():
        wish = request.GET.get('wish')

        user = MyUser.objects.get(id=request.user.id)
        # 위시리스트 추가 시
        if wish:
            # product 조회 및 없을 시 404
            product = get_object_or_404(Product, id=wish)

            # wish 객체 검색 또는 생성
            wish_list, created = WishList.objects.get_or_create(
                user=user,
                item=product
            )

            if created:
                # num_heart 증가
                product.num_heart += 1
                product.save()
                seller.total_num_heart += 1
                seller.save()

                data = {
                    "status": "success"
                }
            else:
                wish_list.delete()
                product.num_heart += -1
                product.save()
                seller.total_num_heart += -1
                seller.save()
                data = {
                    "status": "fail"
                }
            return HttpResponse(json.dumps(data), content_type='application/json')

        if request.method == 'POST':
            # 상품 상세 페이지에서 장바구니 추가
            if request.POST['action'] == 'cart':
                cart_items = request.POST.getlist('cart[]')
                if cart_items:
                    data = add_to_cart(request, product, cart_items)
                    if data is not None:
                        return HttpResponse(json.dumps(data), content_type='application/json')
                    else:
                        raise Http404

            # 상품 상세 페이지에서 바로구매
            elif request.POST['action'] == 'purchase':
                cart_items = request.POST.getlist('cart[]')

                if cart_items:
                    # 카트 세션이 남아 있는 경우 제거
                    try:
                        del request.session['cart_id']
                    except KeyError:
                        pass
                    finally:
                        data = add_to_cart(request, product, cart_items)

                    if data is not None:
                        return HttpResponse(json.dumps(data), content_type='application/json')
                    else:
                        raise Http404

    template = 'product/product_detail.html'
    context = {
        'product': product,
        'product_tag':product_tag,
        'count': seller_count,
        'rating': seller_rating,
        'reviews': reviews,
        'reviews_count': reviews_count,
        'is_user_wished':is_user_wished
    }
    return render(request, template, context)


@login_required
def product_upload(request, product_id=None):
    form = ProductForm()
    tag_form = TagForm()

    # 만약 처음 올리는거라면 판매자로 등록
    try:
        seller = Seller.objects.get(user=request.user)
    except:
        seller = Seller(
            user=request.user
        )
        seller.save()

    # 리스트에 모델 담기
    seller_products = Product.objects.filter(seller=seller)

    # 태그 리스트, oneline_intro 리스트 만들기
    seller_tag_list = []
    products_intro_list = []
    for product in seller_products:
        temp_tag = ProductTag.objects.filter(object_id=product.id,
                                             content_type=ContentType.objects.get_for_model(product))
        products_intro_list.append(product.oneline_intro)
        if not temp_tag:
            seller_tag_list.append(temp_tag)
            pass
        else:
            temp_arr = []
            for ta in temp_tag:
                temp_arr.append(ta.tag.encode('utf-8', 'ignore'))
            seller_tag_list.append(temp_arr)

    # 리스트에 있는 모델들을 순회하며 json타입으로
    json_seller_products = [res.as_json().encode('utf-8', 'ignore') for res in seller_products]

    json_arr = [res[1:-1] for res in json_seller_products]

    # 저장하기 눌렀을 경우
    if request.method == 'POST':
        form = ProductForm(request.POST or None, request.FILES or None)
        tag_form = TagForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.seller = seller
            instance.save()
            if tag_form.is_valid():
                tags = request.POST.getlist('tag')
                for tag in tags:
                    related_object_type = ContentType.objects.get_for_model(instance)
                    ProductTag.objects.create(
                        tag=tag,
                        content_type=related_object_type,
                        object_id=instance.id
                    )

            #return HttpResponseRedirect('/dashboard/')
            return HttpResponseRedirect('/')

        else:
            pass

    type_ = "등록"

    template = 'product/product_upload.html'
    context = {
        "form": form,
        "tag_form": tag_form,
        "type_": type_,
        "seller_products": json_arr,
        "tags": seller_tag_list,
        "oneline_intros": products_intro_list
    }
    return render(request, template, context)


@login_required
def product_upload_complete(request):
    template = 'product/product_upload_complete.html'
    context = {

    }

    return render(request, template, context)


@login_required
def product_manage(request):
    # 판매자가 아닐 경우
    try:
        seller = Seller.objects.get(user=request.user)
    except:
        seller = None

    if seller is None:
        messages.warning(request, '판매자가 아닙니다. 상품 등록 시 자동으로 판매자 등록이 됩니다.')
        product_list = None
    else:
        product_list = Product.objects.filter(seller=seller).exclude(product_status='terminated')

    order_item_status_list = []

    for product in product_list:
        if product.product_status == 'ready':
            order_item_status_list.append('x')
        else:
            temp_cart_item = CartItem.objects.filter(item=product)
            temp_order_item = OrderItem.objects.filter(cart_item=temp_cart_item)
            order_item_status_list.append(temp_order_item)

    template = 'seller/product_manage.html'
    context = {
        "product_list": product_list,
        "order_item_status_list": order_item_status_list
    }

    return render(request, template, context)


@login_required
def product_change(request, product_id):
    # ID로 상품 조회
    product = get_object_or_404(Product, id=product_id)
    # 상품 아이템 조회
    related_object_type = ContentType.objects.get_for_model(product)

    # 유저가 판매자인지 체크
    if product.seller.user != request.user:
        # 판매자가 아니면 404 에러 호출
        raise Http404

    try:
        # product tag
        tags = ProductTag.objects.filter(content_type=related_object_type, object_id=product_id)
    except ProductTag.DoesNotExist:
        raise Http404

    tag_list = []
    for item in tags:
        tag_list.append(item.tag)


    form = ProductForm(instance=product)

    tag_form = TagForm(initial={
        "tag": tag_list
    })

    type_ = "수정"

    seller = Seller.objects.filter(user=request.user)[0]
    # 리스트에 모델 담기
    seller_products = Product.objects.filter(seller=seller)

    # 태그 리스트, oneline_intro 리스트 만들기
    seller_tag_list = []
    products_intro_list = []
    for product in seller_products:
        temp_tag = ProductTag.objects.filter(object_id=product.id,
        content_type=ContentType.objects.get_for_model(product))
        products_intro_list.append(product.oneline_intro)
        if not temp_tag:
            seller_tag_list.append(temp_tag)
            pass
        else:
            temp_arr = []
            for ta in temp_tag:
                temp_arr.append(ta.tag.encode('utf-8', 'ignore'))
            seller_tag_list.append(temp_arr)

    # 리스트에 있는 모델들을 순회하며 json타입으로
    json_seller_products = [res.as_json().encode('utf-8','ignore') for res in seller_products]

    json_arr = [res[1:-1] for res in json_seller_products]

    if request.method == 'POST':
        form = ProductForm(request.POST or None, request.FILES or None, instance=product)
        tag_form = TagForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.seller = seller
            instance.save()
            if tag_form.is_valid():
                old_tags = ProductTag.objects.filter(object_id=instance.id)
                for old_tag in old_tags:
                    old_tag.delete(using=None, keep_parents=False)

                tags = request.POST.getlist('tag')
                for tag in tags:
                    related_object_type = ContentType.objects.get_for_model(instance)

                    ProductTag.objects.create(
                        tag=tag,
                        content_type=related_object_type,
                        object_id=instance.id
                    )

            return HttpResponseRedirect('/')

        else:
            pass

    template = 'product/product_edit.html'

    context = {
        "form": form,
        "tag_form": tag_form,
        "type_": type_,
        "seller_products":json_arr,
        "tags":seller_tag_list,
        "oneline_intros": products_intro_list
    }

    return render(request, template, context)


@login_required
def product_delete(request, product_id):
    print('product_delete')
    #product_id = request.GET.get('delete_product')
    product_id = product_id
    # checking delete validation
    product = get_object_or_404(Product, id=product_id)

    if product.seller.user != request.user:
        raise Http404

    # disable the product
    product.product_status = "terminated"
    product.save()

    return redirect(reverse('product_manage'))


@login_required
def product_order_manage(request):
    if request.POST.get('is_status_change'):
        order_item_id = request.POST.get('order_item')
        try:
            order_item = OrderItem.objects.get(id=order_item_id)
            order_item.status = request.POST.get('new_status')
            order_item.save()
        except:
            pass

    try:
        seller = Seller.objects.get(user=request.user)
    except:
        seller = None

    if seller:
        order_items = OrderItem.objects.filter(user=request.user)
        order_items_ready = order_items.filter(user=request.user, status='paid')
        order_items_processing = order_items.filter(user=request.user, status='processing')
        order_items_finished = order_items.filter(user=request.user, status='finished')
        order_items_wait_confirm = order_items.filter(user=request.user, status='wait_confirm')
        order_items_refunded = order_items.filter(user=request.user, status='refunded')
        order_items_request_refund = order_items.filter(user=request.user, status='request_refund')

        template = 'seller/order_manage.html'
        context = {
            "order_items": order_items,
            "order_items_ready": order_items_ready,
            "order_items_processing": order_items_processing,
            "order_items_finished": order_items_finished,
            "order_items_wait_confirm": order_items_wait_confirm,
            "order_items_refunded": order_items_refunded,
            "order_items_request_refund": order_items_request_refund,
            "order_items_request_refund_length": order_items_request_refund.count(),
        }

        return render(request, template, context)
    else:
        return HttpResponseRedirect('/dashboard/')


@login_required
def product_profit_manage(request):
    try:
        seller = Seller.objects.get(user=request.user)
    except:
        seller = None

    if seller:
        profits = Profit.objects.filter(seller=seller)
        expected_profit = profits.filter(seller=seller, type="expect_profit").aggregate(Sum('money'))['money__sum']
        possible_profit = profits.filter(seller=seller, type="possible_profit").aggregate(Sum('money'))['money__sum']
        requested_profit = profits.filter(seller=seller, type="requested_profit").aggregate(Sum('money'))['money__sum']
        completed_profit = profits.filter(seller=seller, type="completed_profit").aggregate(Sum('money'))['money__sum']

        if expected_profit is None:
            expected_profit = 0

        if possible_profit is None:
            possible_profit = 0

        if requested_profit is None:
            requested_profit = 0

        if completed_profit is None:
            completed_profit = 0

        # SellerAccount, Withdrawal 폼
        s_account, s_created = SellerAccount.objects.get_or_create(seller=seller)
        if request.method == 'POST':
            if request.POST.get('account_change'):
                s_account_form = SellerAccountForm(request.POST, instance=s_account)

                if s_account_form.is_valid():
                    s_account_form_instance = s_account_form.save(commit=False)
                    try:
                        s_account_form_instance.seller = seller
                    except:
                        pass
                    s_account_form_instance.save()

                    return HttpResponseRedirect('/product/profit/')

            if request.POST.get('withdraw'):
                withdrawal = Withdrawal.objects.create(seller=seller, seller_account=s_account, status="request")
                withdrawal_form = WithdrawalForm(request.POST, instance=withdrawal)

                if withdrawal_form.is_valid():
                    # 출금 요청액이 출금 가능액을 초과하거나 음수인 경우
                    if int(request.POST.get('money')) > int(possible_profit) or int(request.POST.get('money')) < 0:
                        raise Http404

                    withdrawal_form_instance = withdrawal_form.save(commit=False)
                    try:
                        withdrawal_form_instance.seller = seller
                    except:
                        pass
                    withdrawal_form_instance.save()

                    return HttpResponseRedirect('/product/profit/')
        else:
            s_account_form = SellerAccountForm(instance=s_account)
            withdrawal_form = WithdrawalForm()

        template = 'seller/profit_manage.html'
        context = {
            "seller_account_forms" : s_account_form,
            "withdrawal_forms" : withdrawal_form,
            "expected_profit": expected_profit,
            "possible_profit": possible_profit,
            "requested_profit": requested_profit,
            "completed_profit": completed_profit,
        }

        return render(request, template, context)
    else:
        return HttpResponseRedirect('/dashboard/')
