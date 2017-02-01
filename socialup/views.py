# -*- coding: utf-8 -*-
# django import
from django.shortcuts import (
    render,
    render_to_response,
    HttpResponse,
)
from django.template import RequestContext
from django.contrib.contenttypes.models import ContentType


# app import
from markets.models import Product, sns_type_list

import json


def home(request):
    template = 'home.html'

    # 처음 상품
    # 평점순
    products_by_rating = Product.objects.all().active().order_by('-rating')[:20]
    # 최신순
    products_by_created = Product.objects.all().active().order_by('-created')[:20]
    # 가격순
    products_by_created = Product.objects.all().active().order_by('-price')[:20]

    context = {
        "products_rating": products_by_rating,
        "products_created": products_by_created,
    }

    return render(request, template, context)


def product_category(request, category):
    if category=="all":
        products = Product.objects.active().all()
    else:
        products = Product.objects.active().filter(sns_type=category)

    if request.is_ajax():
        checked_tags = json.loads(request.GET['checked_tags'])

        products_by_tags = []
        for tag in checked_tags:
            products_by_tags.extend(products.active().filter(product_tag__tag=tag))

        # 중복된 아이템 제거
        products_by_tags = list(set(products_by_tags))

        product_ids_by_tags = []
        for product in products_by_tags:
            product_ids_by_tags.append(product.id)

        data = {
            "product_ids_by_tags": product_ids_by_tags,
        }

        return HttpResponse(json.dumps(data), content_type='application/json')


    category_name = [type_[1] for type_ in sns_type_list if type_[0] == category][0]

    # 평점순
    products_by_rating = products.active().order_by('-rating')
    # 최신순
    products_by_created = products.active().order_by('-created')
    # 가격순
    products_by_price = products.active().order_by('-price')

    template = 'category.html'
    context = {
        "category": category_name,
        "products_rating": products_by_rating,
        "products_created": products_by_created,
        "products_price": products_by_price,
    }

    return render(request, template, context)


def product_search(request):
    keyword = request.GET['keyword']
    products = Product.objects.active().filter(oneline_intro__contains=keyword)

    # 평점순
    products_by_rating = products.active().order_by('-rating')
    # 최신순
    products_by_created = products.active().order_by('-created')
    # 가격순
    products_by_price = products.active().order_by('-price')

    template = 'search.html'
    context = {
        "keyword": keyword,
        "products_rating": products_by_rating,
        "products_created": products_by_created,
    }

    return render(request, template, context)


# Http Error 400
def bad_request(request):
    response = render_to_response(
        'error/400.html',
        context_instance=RequestContext(request)
    )

    response.status_code = 400

    return response


# Http Error 403
def permission_denied(request):
    response = render_to_response(
        'error/403.html',
        context_instance=RequestContext(request)
    )

    response.status_code = 403

    return response


# Http Error 404
def page_not_found(request):
    response = render_to_response(
        'error/404.html',
        context_instance=RequestContext(request)
    )

    response.status_code = 404

    return response


# Http Error 500
def server_error(request):
    response = render_to_response(
        'error/500.html',
        context_instance=RequestContext(request)
    )

    response.status_code = 500

    return response
