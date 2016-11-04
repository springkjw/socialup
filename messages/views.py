# -*- coding: utf-8 -*-
from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from accounts.models import MyUser

@login_required
def message_lounge(request):
    template = 'message/message_lounge.html'
    return render(request, template)

@login_required
def message_room(request):
    template = 'message/message_room.html'
    return render(request, template)
