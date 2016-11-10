# -*- coding: utf-8 -*-
from django.shortcuts import (
    render,
    HttpResponse,
    Http404,
    HttpResponseRedirect,
    get_object_or_404,
    redirect,
)
from django.contrib import messages
from django.forms import inlineformset_factory
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.forms import generic_inlineformset_factory
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from .models import (
    Product,
    Variation,
    ProductTag,
    SnsType,
    ProductTarget,
    SnsUrl,
)
from .forms import ProductForm, VariationForm, TagForm, TypeForm, TargetForm, SnsForm
from carts.models import WishList
from carts.views import add_to_cart
from billing.models import Order, ProductManage
from accounts.models import MyUser, Seller
from reviews.models import ProductReview

import json


@login_required
def product_detail(request, product_id):
    # product_id로 상품 조회
    product_instance = Product.objects.active()
    product = get_object_or_404(product_instance, id=product_id)
    # product 판매자
    seller = product.seller
    # product 판매자 평점 조회
    seller_rating = int(round(seller.rating * 20))
    seller_count = Product.objects.filter(seller=seller).count()

    variation = Variation.objects.filter(
        product=product
    )

    # Product 중 기본가에 해당하는 아이템
    try:
        default = variation.get(is_default=True)
    except:
        default = None

    reviews = ProductReview.objects.filter(product=product)
    reviews_count = reviews.count()

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
                data = {
                    "status": "success"
                }
            else:
                data = {
                    "status": "fail"
                }

            return HttpResponse(json.dumps(data), content_type='application/json')

        if request.method == 'POST':
            if request.POST['action'] == 'cart':
                cart = request.POST.getlist('cart[]')

                if cart:
                    cart = add_to_cart(request, default, cart)

                    if cart is not None:
                        data = {
                            "status": "success",
                        }

                        return HttpResponse(json.dumps(data), content_type='application/json')
                    else:
                        raise Http404

            elif request.POST['action'] == 'purchase':
                option = request.POST.getlist('cart[]')

                if option:
                    # 카트 세션이 남아 있는 경우 제거
                    try:
                        del request.session['cart_id']
                    finally:
                        cart = add_to_cart(request, default, option)

                    if cart is not None:
                        data = {
                            "status": "success",
                            "cart_id": cart.id
                        }

                        return HttpResponse(json.dumps(data), content_type='application/json')
                    else:
                        raise Http404

    template = 'product/product_detail.html'
    context = {
        'product': product,
        'count': seller_count,
        'variation': variation,
        'default_price': default,
        'rating': seller_rating,
        'reviews': reviews,
        'reviews_count': reviews_count
    }

    return render(request, template, context)


@login_required
def product_upload(request, product_id=None):
    VariationInlineFormset = inlineformset_factory(Product, Variation, form=VariationForm, extra=1, )

    form = ProductForm()
    formset = VariationInlineFormset()
    tag_form = TagForm()
    type_form = TypeForm()
    target_form = TargetForm()
    url_form = SnsForm()

    # 저장하기 눌렀을 경우
    if request.method == 'POST':
        # 만약 처음 올린거라면 판매자로 등록
        try:
            seller = Seller.objects.get(user=request.user)
        except:
            seller = Seller(
                user=request.user
            )
            seller.save()

        form = ProductForm(request.POST or None, request.FILES or None)
        tag_form = TagForm(request.POST)
        type_form = TypeForm(request.POST)
        target_form = TargetForm(request.POST)
        url_form = SnsForm(request.POST)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.seller = seller
            instance.save()

            # save sns url
            url_list = request.POST.getlist('url')
            url_active_list = request.POST.get('url_is_active')
            if url_active_list:
                is_active = False
            else:
                is_active = True
            for url in url_list:
                related_object_type = ContentType.objects.get_for_model(instance)
                SnsUrl.objects.create(
                    url=url,
                    is_active=is_active,
                    content_type=related_object_type,
                    object_id=instance.id
                )

            # Variations Checking
            formset = VariationInlineFormset(request.POST, instance=instance)
            if formset.is_valid():
                formset.save()
            else:
                print formset.errors

            if tag_form.is_valid():
                tags = request.POST.getlist('tag')
                for tag in tags:
                    related_object_type = ContentType.objects.get_for_model(instance)
                    ProductTag.objects.create(
                        tag=tag,
                        content_type=related_object_type,
                        object_id=instance.id
                    )

            if type_form.is_valid():
                types = request.POST.getlist('type')
                for type in types:
                    related_object_type = ContentType.objects.get_for_model(instance)
                    SnsType.objects.create(
                        type=type,
                        content_type=related_object_type,
                        object_id=instance.id
                    )

            if target_form.is_valid():
                targets = request.POST.getlist('target')
                for target in targets:
                    related_object_type = ContentType.objects.get_for_model(instance)
                    ProductTarget.objects.create(
                        target=target,
                        content_type=related_object_type,
                        object_id=instance.id
                    )

            return HttpResponseRedirect('/dashboard/')

        else:
            pass

    type_ = "등록"

    template = 'product/product_upload.html'
    context = {
        "form": form,
        "formset": formset,
        "tag_form": tag_form,
        "type_form": type_form,
        "target_form": target_form,
        "url_form": url_form,
        "type_": type_
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
        product_list = Product.objects.filter(seller=seller).active()

    template = 'seller/product_manage.html'
    context = {
        "product_list": product_list
    }

    return render(request, template, context)


@login_required
def product_change(request, product_id):
    # ID로 상품 조회
    product = get_object_or_404(Product, id=product_id)
    # 상품 아이템 조회
    variation = Variation.objects.filter(product=product)
    related_object_type = ContentType.objects.get_for_model(product)

    # 유저가 판매자인지 체크
    if product.seller.user != request.user:
        # 판매자가 아니면 404 에러 호출
        raise Http404

    try:
        # product tag
        tags = ProductTag.objects.filter(content_type=related_object_type, object_id=product_id)
        # product type
        types = SnsType.objects.filter(content_type=related_object_type, object_id=product_id)
        # product target
        targets = ProductTarget.objects.filter(content_type=related_object_type, object_id=product_id)
        # product sns url
        urls = SnsUrl.objects.filter(content_type=related_object_type, object_id=product_id)
    except ProductTag.DoesNotExist:
        raise Http404
    except SnsType.DoesNotExist:
        raise Http404
    except ProductTarget.DoesNotExist:
        raise Http404
    except SnsUrl.DoesNotExist:
        raise Http404

    tag_list = []
    for item in tags:
        tag_list.append(item.tag)

    type_list = []
    for item in types:
        type_list.append(item.type)

    target_list = []
    for item in targets:
        target_list.append(item.target)

    url_list = []
    for item in urls:
        url_list.append(item.url)

    form = ProductForm(instance=product)

    VariationInlineFormset = inlineformset_factory(Product, Variation, form=VariationForm, extra=0)
    formset = VariationInlineFormset(instance=product)

    UrlInlineFormset = generic_inlineformset_factory(SnsUrl, extra=0)
    url_formset = UrlInlineFormset(instance=product)

    tag_form = TagForm(initial={
        "tag": tag_list
    })
    type_form = TypeForm(initial={
        "type": type_list
    })
    target_form = TargetForm(initial={
        "target": target_list
    })
    url_form = SnsForm(initial={
        "url": url_list[0]
    })

    type_ = "수정"

    if request.method == 'POST':
        form = ProductForm(request.POST or None, request.FILES or None)

    template = 'product/product_upload.html'

    context = {
        "form": form,
        "formset": formset,
        "tag_form": tag_form,
        "type_form": type_form,
        "target_form": target_form,
        "url_form": url_form,
        "url_list": url_list,
        "url_formset": url_formset,
        "type_": type_
    }

    return render(request, template, context)


@login_required
def product_delete(request):
    product_id = request.GET.get('delete_product')
    # checking delete validation
    product = get_object_or_404(Product, id=product_id)

    if product.seller.user != request.user:
        raise Http404

    # disable the product
    product.is_active = False
    product.save()

    return redirect(reverse('product_manage'))


@login_required
def product_order_manage(request):
    purchase_list = Order.objects.filter(user=request.user)
    status_0 = purchase_list.filter(status='paid').count()
    status_1 = purchase_list.filter(status='processing').count()
    status_2 = purchase_list.filter(status='finished').count()
    status_3 = purchase_list.filter(status='refunded').count()

    template = 'seller/order_manage.html'
    context = {
        "orders": purchase_list,
        "status_0": status_0,
        "status_1": status_1,
        "status_2": status_2,
        "status_3": status_3,
    }

    return render(request, template, context)
