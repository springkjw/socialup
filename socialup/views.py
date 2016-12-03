# -*- coding: utf-8 -*-
# django import
from django.shortcuts import (
    render,
    render_to_response,
)
from django.template import RequestContext
from django.contrib.contenttypes.models import ContentType


# app import
from markets.models import Product, sns_type, SnsType
from markets.forms import (
    TagForm,
    TargetForm,
    SnsTypeForm,
)


def home(request):
    template = 'home.html'

    # 처음 상품
    # 평점순
    products_by_rating = Product.objects.all().active().order_by('-rating')[:20]
    # 최신순
    products_by_created = Product.objects.all().active().order_by('-created')[:20]

    tag_form = TagForm()
    target_form = TargetForm()
    sns_form = SnsTypeForm()

    # 검색 필터링
    if request.method == 'POST':
        tag_form = TagForm(request.POST)
        target_form = TargetForm(request.POST)
        sns_form = SnsTypeForm(request.POST)

        if tag_form.is_valid() and target_form.is_valid() and sns_form.is_valid():
            tag = tag_form.cleaned_data.get('tag')
            target = target_form.cleaned_data.get('target')
            sns = sns_form.cleaned_data.get('sns')

            products = Product.objects.filter(tags__tag__in=tag, target__target__in=target, type__type__in=sns).active()

            if not products:
                # 필터링 결과가 아무 것도 없을 경우 랜덤으로 10개 반환
                products = Product.objects.all().active().order_by('?')[:8]
                message = "검색 결과가 아무 것도 없네요. 다른 상품들을 보시겠어요?"

                context = {
                    "products": products,
                    "tag_form": tag_form,
                    "target_form": target_form,
                    "sns_form": sns_form,
                    "message": message,
                }
                print(context)
                return render(request, template, context)

    context = {
        "products_rating": products_by_rating,
        "products_created": products_by_created,
        "tag_form": tag_form,
        "target_form": target_form,
        "sns_form": sns_form,
    }

    return render(request, template, context)


def product_category(request, category):
    products = Product.objects.filter(type__type=category)

    category_name = [type_[1] for type_ in sns_type if type_[0] == category][0]

    # 처음 상품
    # 평점순
    products_by_rating = products.order_by('-rating')
    # 최신순
    products_by_created = products.order_by('-created')

    template = 'category.html'
    context = {
        "category": category_name,
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
