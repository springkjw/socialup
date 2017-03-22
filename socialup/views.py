# -*- coding: utf-8 -*-
# django import
from django.shortcuts import (
    render,
    render_to_response,
    HttpResponse,
)
from django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q

# app import
from markets.models import Product, sns_type_list

import json


def home(request):
    order = request.GET.get('order') or 'rating'

    products = Product.objects.active().order_by('-' + order)

    if products.exists():
        try:
            highest_price = products.order_by('price').reverse()[0].price
            lowest_price = products.order_by('price')[0].price
        except IndexError:
            highest_price = 10000
            lowest_price = 0

        if highest_price == lowest_price:
            high_low = [highest_price, 0]
        else:
            high_low = [highest_price, lowest_price]
    else:
        highest_price = 0
        lowest_price = 0
        high_low = [highest_price, lowest_price]

    products = products[:12]
    template = 'home.html'
    context = {
        "products": products,
        "high_low": high_low,
    }

    return render(request, template, context)


def product_category(request):
    category = request.GET.get('category') or 'all'
    tags = request.GET.getlist('tag')
    order = request.GET.get('order') or 'rating'
    page = request.GET.get('page')

    products = Product.objects.all().active()
    if category == 'all':
        category_name = "전체"
    else:
        products = Product.objects.filter(sns_type=category)
        category_name = [type_[1] for type_ in sns_type_list if type_[0] == category][0]

    tag_params = ""
    if "all" not in tags:
        tag_q = Q()
        for tag in tags:
            tag_q.add(Q(product_tag__tag=tag), Q.OR)
            tag_params += "&tag=" + tag
        products = products.filter(tag_q).distinct()

    try:
        highest_price = products.order_by('price').reverse()[0].price
        lowest_price = products.order_by('price')[0].price
    except IndexError:
        highest_price = 10000
        lowest_price = 0

    price_max = request.GET.get('price_max') or highest_price
    price_min = request.GET.get('price_min') or lowest_price
    products = products.filter(price__gte=price_min, price__lte=price_max)

    if highest_price == lowest_price:
        high_low = [highest_price, 0]
    else:
        high_low = [highest_price, lowest_price]

    # pagination
    products_list = products.order_by('-' + order)
    products_paginator = Paginator(products_list, 20)
    try:
        products = products_paginator.page(page)
    except PageNotAnInteger:
        products = products_paginator.page(1)
    except EmptyPage:
        products = products_paginator.page(products_paginator.num_pages)

    if products_paginator.num_pages <= 10:
        previous_num = xrange(1, products.number)
        next_num = xrange(products.number + 1, products_paginator.num_pages + 1)
    else:
        if products.number <= 5:
            previous_num = xrange(1, products.number)
            next_num = xrange(products.number + 1, 11)
        elif products.number >= products_paginator.num_pages - 5:
            previous_num = xrange(products_paginator.num_pages - 9, products.number)
            next_num = xrange(products.number + 1, products_paginator.num_pages + 1)
        else:
            previous_num = xrange(products.number - 5, products.number)
            next_num = xrange(products.number + 1, products.number + 5)

    template = "category/category.html"
    context = {
        "category_name": category_name,
        "tags": tags,
        "tag_params": tag_params,
        "products": products,
        "high_low": high_low,
        "price_max": price_max,
        "price_min": price_min,
        "previous_num": previous_num,
        "next_num": next_num
    }

    return render(request, template, context)


def product_search(request):
    keyword = request.GET['keyword']
    search_option = request.GET['search_option']

    if search_option == 'integrated_search':
        products = Product.objects.active().filter(
            Q(oneline_intro__contains=keyword) | Q(seller__user__email__iregex=keyword + '@' + r'.*$'))
    elif search_option == 'sns_all':
        products = Product.objects.active().filter(oneline_intro__contains=keyword)
    elif search_option == 'sns_blog':
        products = Product.objects.active().filter(sns_type='blog', oneline_intro__contains=keyword)
    elif search_option == 'sns_facebook':
        products = Product.objects.active().filter(sns_type='facebook', oneline_intro__contains=keyword)
    elif search_option == 'sns_instagram':
        products = Product.objects.active().filter(sns_type='instagram', oneline_intro__contains=keyword)
    elif search_option == 'sns_youtube':
        products = Product.objects.active().filter(sns_type='youtube', oneline_intro__contains=keyword)
    elif search_option == 'seller_id':
        # products = Product.objects.active().filter(seller__user__email__iregex=keyword + '@' + r'.*$')
        products = Product.objects.active().filter(seller__user__name__contains=keyword)
    else:
        products = Product.objects.active().filter(oneline_intro__contains=keyword)

    # 평점순
    products_by_rating = products.active().order_by('-rating')
    # 최신순
    products_by_created = products.active().order_by('-created')
    # 가격순
    products_by_price = products.active().order_by('-price')

    template = 'search.html'
    context = {
        # "search_option" : search_option,
        "keyword": keyword,
        "products_rating": products_by_rating,
        "products_created": products_by_created,
        "products_price": products_by_price,
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
