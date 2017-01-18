# -*- coding: utf-8 -*-
from django.shortcuts import render, HttpResponseRedirect
from django.contrib import messages
from django.core.urlresolvers import reverse
from .models import MyUser, Seller
from .forms import ChangeForm
from django.contrib.auth import authenticate, login



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

def change_info(request):
    user = MyUser.objects.get(id=request.user.id)
    form = ChangeForm()
    template = 'account/account_change.html'


    if request.method == "POST":
        form = ChangeForm(request.POST or None, request.FILES or None)
        password_success = user.check_password(request.POST['current_passwd'])

        if not password_success:
            error_message = "입력하신 비밀번호가 틀렸습니다."
            context= {
                "error_message":error_message,
                "form": form,
                "year_list": year_list,
                "address_list":address_list,
            }
            return render(request, template, context)

        if form.is_valid():
            print(password_success)

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

            return HttpResponseRedirect('/dashboard/change/')

    context = {
        "form": form,
        "year_list": year_list,
        "address_list":address_list,
    }

    return render(request, template, context)


def login_cancelled(request):
    messages.error(request, "페이스북 연결이 취소 되었습니다. 다시 시도해주세요.")
    return HttpResponseRedirect(reverse('account_signup'))