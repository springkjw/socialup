# -*- coding: utf-8 -*-
# django import
from django.shortcuts import (
    render,
    render_to_response,
    HttpResponse,
)
from django.template import RequestContext
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q

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
    products_by_price = Product.objects.all().active().order_by('-price')[:20]

    context = {
        "products_rating": products_by_rating,
        "products_created": products_by_created,
        "products_price": products_by_price,
    }

    return render(request, template, context)


def product_category(request, category):
    if category=="all":
        products = Product.objects.active().all()
        category_name = "전체"
    else:
        products = Product.objects.active().filter(sns_type=category)
        category_name = [type_[1] for type_ in sns_type_list if type_[0] == category][0]

    if request.is_ajax():
        checked_tags = json.loads(request.GET['checked_tags'])
        
        if 'all' in checked_tags:
            products_by_tags = []
            products_by_tags.extend(products)
        else:
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

    # test용. 템플릿에서 request.GET['search_option']를 던져줄 수 있으면 아래 한줄을 지우고 나머지 주석을 모두 해제
    products = Product.objects.active().filter(Q(oneline_intro__contains=keyword) | Q(seller__user__email__iregex=keyword + '@' + r'.*$'))

    # search_option = request.GET['search_option']
    #
    # if search_option == 'integrated_search':
    #     products = Product.objects.active().filter(Q(oneline_intro__contains=keyword) | Q(seller__user__email__iregex=keyword + '@' + r'.*$'))
    # elif search_option == 'sns_all':
    #     products = Product.objects.active().filter(oneline_intro__contains=keyword)
    # elif search_option == 'sns_facebook':
    #     products = Product.objects.active().filter(sns_type='facebook', oneline_intro__contains=keyword)
    # elif search_option == 'sns_facebook':
    #     products = Product.objects.active().filter(sns_type='blog', oneline_intro__contains=keyword)
    # elif search_option == 'sns_instagram':
    #     products = Product.objects.active().filter(sns_type='instagram', oneline_intro__contains=keyword)
    # elif search_option == 'sns_kakaostory':
    #     products = Product.objects.active().filter(sns_type='kakaostory', oneline_intro__contains=keyword)
    # elif search_option == 'seller_id':
    #     products = Product.objects.active().filter(seller__user__email__iregex=keyword + '@' + r'.*$')
    # else:
    #     products = Product.objects.active().filter(oneline_intro__contains=keyword)

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
