from django.shortcuts import render
from apps.store.models import Category , Product 

# Create your views here.

def order_confirmation(request):
    return render(request,'order_confirmation.html')

def frontpage(request):
    products = Product.objects.filter(is_featured=True)
    featured_category = Category.objects.filter(is_featured=True)
    popular_products = Product.objects.all().order_by('-num_visits')[0:10]
    recently_viewed_products = Product.objects.all().order_by('-last_visit')[0:4]
    top_products = Product.objects.filter(top_product=True)[0:1]

    context = {
        'products':products,
        'featured_category':featured_category,
        'popular_products':popular_products,
        'recently_viewed_products':recently_viewed_products,
        'top_products':top_products
        
    }
    return render(request,'frontpage.html',context)

def contact(request):
    return render(request,'contact.html')

def about(request):
    return render(request,'about.html')

    