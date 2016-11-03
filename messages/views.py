# -*- coding: utf-8 -*-
from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from accounts.models import MyUser

@login_required
def message_lounge(request):
    user = MyUser.objects.get(id=request.user.id)

    template = 'message/message_lounge.html'
    context = {}

    return render(request, template, context)

@login_required
def message_room(request):
    user = MyUser.objects.get(id=request.user.id)

    template = 'message/message_room.html'
    context = {}

    return render(request, template, context)
