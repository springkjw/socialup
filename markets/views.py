# -*- coding: utf-8 -*-
from django.shortcuts import render, HttpResponse, Http404, HttpResponseRedirect, get_object_or_404
from django.contrib import messages
from django.forms import inlineformset_factory
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required
from .models import Product, Variation, ProductTag, SnsType, ProductTarget, SnsUrl
from .forms import ProductForm, VariationForm, TagForm, TypeForm, TargetForm
from carts.models import WishList
from carts.views import add_to_cart
from accounts.models import MyUser, Seller
from reviews.models import ProductReview

import json


@login_required
def product_detail(request, product_id):
    # product_id로 상품 조회
    product = Product.objects.get(id=product_id)
    # product의 판매자
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

    # sns_info = Sns.objects.get(product=product)

    reviews = ProductReview.objects.filter(product=product)
    reviews_count = reviews.count()

    if request.is_ajax():
        user = MyUser.objects.get(id=request.user.id)
        wish = request.GET.get('wish')
        cart = request.GET.get('cart[]')

        if wish:
            wishlist, created = WishList.objects.get_or_create(
                user=user,
                item__id=wish
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
        elif cart:
            cart = add_to_cart(request, default, cart)

            if cart is not None:
                data = {
                    "status": "success"
                }

                return HttpResponse(json.dumps(data), content_type='application/json')
            else:
                raise Http404

        if request.method == 'POST':
            option = request.POST.getlist('cart[]')

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

    template = 'product/product_detail.html'
    context = {
        'product': product,
        'count': seller_count,
        'variation': variation,
        'default_price': default,
        'rating': seller_rating,
        # 'sns': sns_info,
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
            else:
                print tag_form.errors

            if type_form.is_valid():
                types = request.POST.getlist('type')
                for type in types:
                    related_object_type = ContentType.objects.get_for_model(instance)
                    SnsType.objects.create(
                        type=type,
                        content_type=related_object_type,
                        object_id=instance.id
                    )
            else:
                print type_form.errors

            if target_form.is_valid():
                targets = request.POST.getlist('target')
                for target in targets:
                    related_object_type = ContentType.objects.get_for_model(instance)
                    ProductTarget.objects.create(
                        target=target,
                        content_type=related_object_type,
                        object_id=instance.id
                    )
            else:
                print target_form.errors

            return HttpResponseRedirect('/dashboard/')

        else:
            pass

    template = 'product/product_upload.html'
    context = {
        "form": form,
        "formset": formset,
        "tag_form": tag_form,
        "type_form": type_form,
        "target_form": target_form
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
        product_list = Product.objects.filter(seller=seller)

    template = 'seller/product_manage.html'
    context = {
        "product_list": product_list
    }

    return render(request, template, context)


@login_required
def product_change(request, product_id):
    # retrieve product by id
    product = get_object_or_404(Product, id=product_id)
    related_object_type = ContentType.objects.get_for_model(product)

    # checking product seller
    if product.seller.user != request.user:
        raise Http404

    # product tag
    tags = ProductTag.objects.filter(content_type=related_object_type, object_id=product_id)
    tag_list = []
    for item in tags:
        tag_list.append(item.tag)

    # product type
    types = SnsType.objects.filter(content_type=related_object_type, object_id=product_id)
    type_list = []
    for item in types:
        type_list.append(item.type)

    # product target
    targets = ProductTarget.objects.filter(content_type=related_object_type, object_id=product_id)
    target_list = []
    for item in targets:
        target_list.append(item.target)

    form = ProductForm(instance=product)
    tag_form = TagForm(initial={
        "tag": tag_list
    })
    type_form = TypeForm(initial={
        "type": type_list
    })
    target_form = TargetForm(initial={
        "target": target_list
    })

    template = 'product/product_upload.html'
    context = {
        "form": form,
        "tag_form": tag_form,
        "type_form": type_form,
        "target_form": target_form
    }

    return render(request, template, context)
