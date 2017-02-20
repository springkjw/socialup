# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from .models import MyUser, Seller, SellerAccount
from .forms import ChangeForm, ChangeSellerForm, ChangeSellerAccountForm
from django.contrib.auth import authenticate, login

from reviews.models import ProductReview
from billing.models import OrderItem, Order
from markets.models import Product

import json


@login_required
def dashboard(request):
    user = MyUser.objects.get(id=request.user.id)

    try:
        is_seller = Seller.objects.get(user=user)
    except:
        is_seller = None

    template = 'account/account_home.html'
    context = {
        "is_seller": is_seller
    }

    return render(request, template, context)

year_list = []
for i in range(1930, 2003):
    year_list.append(i)

"""
address_list=(
    ("Seoul", "서울"),
    ("Gyeonggi", "경기"),
    ("Incheon", "인천"),
    ("Gangwon", "강원"),
    ("Gyeongnam", "경남"),
    ("Gyeongbuk", "경북"),
    ("Jeonbuk", "전북"),
    ("Jeonnam", "전남"),
    ("Jeju", "제주"),
    ("Chungbuk", "충북"),
    ("Chungnam", "충남"),
    ("etc", "기타")
)
"""

address_list=[ "서울", "경기", "인천", "강원", "경남", "경북", "전북",
               "전남", "제주", "충북", "충남", "기타"]

@login_required
def change_info(request):
    user = MyUser.objects.get(id=request.user.id)
    form = ChangeForm()
    seller_form = ChangeSellerForm()
    seller_account_form = ChangeSellerAccountForm()
    template = 'account/account_change.html'

    try:
        seller = Seller.objects.get(user=request.user)
    except:
        seller = Seller(
            user=request.user
        )
        seller.save()

    try:
        seller_account = SellerAccount.objects.get(seller=seller)
    except:
        seller_account = SellerAccount(
            seller=seller
        )
        seller_account.save()

    if request.is_ajax():
        password_success = user.check_password(request.POST['current_passwd'])
        if request.POST['new_passwd']=='':
            password_success=True
        data = {
            "password_success": password_success
        }
        return HttpResponse(json.dumps(data), content_type='application/json')

    if request.method == "POST":
        form = ChangeForm(request.POST or None, request.FILES or None)
        seller_form = ChangeSellerForm(request.POST or None, request.FILES or None)
        seller_account_form = ChangeSellerAccountForm(request.POST or None, request.FILES or None)

        if seller_form.is_valid():
            seller.type=seller_form.cleaned_data['type']
            seller.company_name=seller_form.cleaned_data['company_name']
            seller.representative_name=seller_form.cleaned_data['representative_name']
            seller.corporate_number=seller_form.cleaned_data['corporate_number']
            seller.business_field=seller_form.cleaned_data['business_field']
            seller.company_type=seller_form.cleaned_data['company_type']
            seller.business_license=seller_form.cleaned_data['business_license']
            seller.account_copy=seller_form.cleaned_data['account_copy']
            seller.save()

        if seller_account_form.is_valid() and 'type' in request.POST:
            seller.type = request.POST['type']
            seller.save()
            seller_account.account_number= seller_account_form.cleaned_data['account_number']
            seller_account.account_name= seller_account_form.cleaned_data['account_name']
            seller_account.bank= seller_account_form.cleaned_data['bank']
            seller_account.save()

            if request.POST['go_main']=='True':
                return HttpResponseRedirect('/')
            else:
                return HttpResponseRedirect('/dashboard/change/')

            return HttpResponseRedirect('/dashboard/change/')
        if form.is_valid():
            password_success = user.check_password(request.POST['current_passwd'])
            if not password_success and request.POST['new_passwd2']:
                error_message = "입력하신 비밀번호가 틀렸습니다."
                context = {
                    "error_message": error_message,
                    "form": form,
                    "seller_form": seller_form,
                    "seller_account_form": seller_account_form,
                    "year_list": year_list,
                    "address_list": address_list,
                    "seller": seller,
                    "seller_account": seller_account,
                }
                return render(request, template, context)


            if form.cleaned_data['media'] != None:
                user.media = form.cleaned_data['media']
            user.name = form.cleaned_data['name']
            user.phone = form.cleaned_data['phone']
            user.description = form.cleaned_data['description']
            user.job = form.cleaned_data['job']
            user.sex = form.cleaned_data['sex']
            user.birth_year = form.cleaned_data['birth_year']
            user.address = form.cleaned_data['address']
            user.agree_purchase_info_email = form.cleaned_data['agree_purchase_info_email']
            user.agree_purchase_info_SMS = form.cleaned_data['agree_purchase_info_SMS']
            user.agree_selling_info_email = form.cleaned_data['agree_selling_info_email']
            user.agree_selling_info_SMS = form.cleaned_data['agree_selling_info_SMS']
            user.agree_marketing_info_email = form.cleaned_data['agree_marketing_info_email']
            user.agree_marketing_info_SMS = form.cleaned_data['agree_marketing_info_SMS']
            new_password = request.POST['new_passwd2']
            if new_password != '' and new_password != request.POST['current_passwd'] and request.POST['new_passwd1'] == request.POST['new_passwd2']:
                user.set_password(new_password)
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request, user)
            user.save()

            if request.POST['go_main']=='True':
                return HttpResponseRedirect('/')
            else:
                return HttpResponseRedirect('/dashboard/change/')

        # !form.is_valid()
        else:
            error_message = "필수항목을 입력해주세요"
            context = {
                "error_message": error_message,
                "form": form,
                "seller_form": seller_form,
                "seller_account_form": seller_account_form,
                "year_list": year_list,
                "address_list": address_list,
                "seller": seller,
                "seller_account": seller_account,
            }
            return render(request, template, context)

    context = {
        "form": form,
        "seller_form": seller_form,
        "seller_account_form":seller_account_form,
        "year_list": year_list,
        "address_list":address_list,
        "seller": seller,
        "seller_account": seller_account,
    }

    return render(request, template, context)


def login_cancelled(request):
    messages.error(request, "페이스북 연결이 취소 되었습니다. 다시 시도해주세요.")
    return HttpResponseRedirect(reverse('account_signup'))

def account_detail(request, seller_id):
    template = 'account/account_detail.html'
    seller= Seller.objects.get(id=seller_id)

    order_item_count = OrderItem.objects.filter(seller=seller, status='finished').count()
    selling_products = Product.objects.filter(seller=seller, product_status="now_selling")
    review_count = 0
    contents_satisfy = [0, 0, 0]
    ad_satisfy = [0, 0, 0]
    kind_satisfy = [0, 0, 0]
    for product in selling_products:
        temp = ProductReview.objects.filter(product=product)
        for review in temp:
            # 컨텐츠 부분
            if review.contents_satisfy == 'good':
                contents_satisfy[0] += 1
            elif review.contents_satisfy == 'neutral':
                contents_satisfy[1] += 1
            else:
                contents_satisfy[2] += 1

            # 광고부분
            if review.ad_satisfy == 'good':
                ad_satisfy[0] += 1
            elif review.ad_satisfy == 'neutral':
                ad_satisfy[1] += 1
            else:
                ad_satisfy[2] += 1

            # 친절도부분
            if review.kind_satisfy == 'good':
                kind_satisfy[0] += 1
            elif review.kind_satisfy == 'neutral':
                kind_satisfy[1] += 1
            else:
                kind_satisfy[2] += 1
        if temp:
            review_count = review_count + len(temp)

    is_seller_none = False
    if (seller.description is None) and (seller.user.sex is None) \
            and (seller.user.birth_year is None) and (len(seller.user.address)==0) and (len(seller.user.job)==0):
        is_seller_none = True

    # 마지막 로그인 시간
    last_login_to_now = datetime.utcnow().replace(tzinfo=None) - seller.user.last_login.replace(tzinfo=None)
    days, seconds = last_login_to_now.days, last_login_to_now.seconds
    last_login_in_hour = days * 24 + seconds // 3600

    context={
        "seller":seller,
        "order_item_count":order_item_count,
        "selling_products":selling_products,
        "is_seller_none": is_seller_none,
        "review_count": review_count,
        "contents_satisfy": contents_satisfy,
        "ad_satisfy": ad_satisfy,
        "kind_satisfy": kind_satisfy,
        "last_login_in_hour": last_login_in_hour,
    }
    return render(request, template, context)