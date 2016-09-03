from django.shortcuts import render
from markets.models import Product

def home(request):
    products = Product.objects.all()

    template = 'home.html'
    context = {
        "products" : products
    }

    return render(request, template, context)