# -*- coding: utf-8 -*-
import json

from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from .models import Report
from .forms import ReportForm

from billing.models import Order


@login_required
def report(request):
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.writer = request.user
            instance.save()

            return HttpResponseRedirect('/dashboard/')
        else:
            pass
    else:
        form = ReportForm()

    template = 'report/report.html'
    context = {
        "forms": form
    }

    return render(request, template, context)


@login_required
def report_history(request):
    reports = Report.objects.filter(writer=request.user)

    template = 'report/report_history.html'
    context = {
        "reports": reports,
    }

    return render(request, template, context)


@login_required
def report_received(request):
    reports = Report.objects.filter(bad_user=request.user)

    template = 'report/report_received.html'
    context = {
        "reports": reports,
    }

    return render(request, template, context)

