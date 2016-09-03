from django.shortcuts import render, HttpResponseRedirect
from allauth.account.adapter import DefaultAccountAdapter
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
        "is_seller" : is_seller
    }

    return render(request, template, context)


def change_info(request):
    user = MyUser.objects.get(id=request.user.id)
    form = ChangeForm(initial={
        'email' : user.email,
        'name' : user.name,
        'phone' : user.phone,
        'description' : user.description
    })

    if request.method == "POST":
        form = ChangeForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            user.media = form.cleaned_data['media']
            user.name = form.cleaned_data['name']
            user.phone = form.cleaned_data['phone']
            user.description = form.cleaned_data['description']
            user.save()

            return HttpResponseRedirect('/dashboard/change/')

    template = 'account/account_change.html'
    context = {
        "form" : form
    }

    return render(request, template, context)


class AccountAdapter(DefaultAccountAdapter):
    def get_login_redirect_url(self, request):
        return '/'