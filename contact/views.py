# -*- coding: utf-8 -*-
import json

from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from .models import Contact
from .forms import ContactForm

from billing.models import Order


@login_required
def contact(request):
    user_type = 'user'
    if request.user.is_seller:
        user_type = 'seller'

    initial = {
        "user_email": request.user.email,
        "user_type": user_type
    }

    if request.method == 'POST':
        form = ContactForm(request.POST, initial=initial)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()

            return HttpResponseRedirect('/dashboard/')
        else:
            pass
    else:
        form = ContactForm(initial=initial)

    if request.is_ajax() and request.method == 'POST':
        order_num = request.POST['order']

        try:
            order_instance = Order.objects.get(order_id=order_num)
        except Order.DoesNotExist:
            order_instance = None

        if order_instance:
            data = {
                "status": "success",
                "message": "주문번호가 확인되었습니다."
            }
        else:
            data = {
                "status": "fail",
                "message": "주문번호를 확인할 수 없습니다."
            }
        return HttpResponse(json.dumps(data), content_type='application/json')

    template = 'contact/contact.html'
    context = {
        "forms": form
    }

    return render(request, template, context)


@login_required
def contact_history(request):
    contact = Contact.objects.filter(user=request.user)

    template = 'contact/contact_history.html'
    context = {
        "contacts": contact,
    }

    return render(request, template, context)
