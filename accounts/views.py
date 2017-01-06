# -*- coding: utf-8 -*-
from django.shortcuts import render, HttpResponseRedirect
from django.contrib import messages
from django.core.urlresolvers import reverse
from .models import MyUser, Seller
from .forms import ChangeForm


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


def change_info(request):
    user = MyUser.objects.get(id=request.user.id)
    form = ChangeForm(initial={
        'email': user.email,
        'name': user.name,
        'phone': user.phone,
        'description': user.description
    })

    if request.method == "POST":
        form = ChangeForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            if form.cleaned_data['media'] != None:
                user.media = form.cleaned_data['media']
            user.name = form.cleaned_data['name']
            user.phone = form.cleaned_data['phone']
            user.description = form.cleaned_data['description']
            user.save()

            return HttpResponseRedirect('/dashboard/change/')

    template = 'account/account_change.html'
    context = {
        "form": form
    }

    return render(request, template, context)


def login_cancelled(request):
    messages.error(request, "페이스북 연결이 취소 되었습니다. 다시 시도해주세요.")
    return HttpResponseRedirect(reverse('account_signup'))