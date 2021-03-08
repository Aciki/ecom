import random
from django.http import request 
from apps.store.models import Product, Category
from django.shortcuts import render , get_object_or_404 , redirect
from .models import Product
from django.db.models import Q
from apps.cart.cart import Cart
from datetime import datetime
from django.core.paginator import Paginator ,EmptyPage , InvalidPage
# Create your views here.


def search(request):
    categories =  Category.objects.all()
    query = request.GET.get('query')
    instock = request.GET.get('instock')
    price_from = request.GET.get('price_from', 0)
    price_to = request.GET.get('price_to', 100000)
    sorting = request.GET.get('sorting', '-date_added')
    f_category = request.GET.get('category',None)
    
    
    
    
    
    products = Product.objects.filter(Q(title__icontains=query) | Q(description__icontains=query)).filter(price__gte=price_from).filter(price__lte=price_to)
    print(query)
    if instock:
        products = products.filter(num_available__gte=1)
    if f_category:
        products =products.filter(category__title  = f_category)




    
    paginator = Paginator(products, 7)
    page_number = request.GET.get('page')
    print (page_number)
    page_obj1 = paginator.get_page(page_number)

    # Get the index of the current page
    index = page_obj1.number - 1  # edited to something easier without index
    # This value is maximum index of your pages, so the last page - 1
    max_index = len(paginator.page_range)
    # You want a range of 7, so lets calculate where to slice the list
    start_index = index - 3 if index >= 3 else 0
    end_index = index + 3 if index <= max_index - 3 else max_index
    # Get our new page range. In the latest versions of Django page_range returns 
    # an iterator. Thus pass it to list, to make our slice possible again.
    page_range = list(paginator.page_range)[start_index:end_index]

        
   
    
   


    context = {
        'query': query,
        'products': products.order_by(sorting),
        'instock': instock,
        'price_from': price_from,
        'price_to': price_to,
        'sorting': sorting,
        'categories':categories,
        # 'count1': count1
        'page_obj1':page_obj1
        
    }

    return render(request, 'search.html', context)



def product_detail(request,category_slug,slug):
    product = get_object_or_404(Product,slug=slug)
    product.num_visits = product.num_visits + 1
    product.last_visit = datetime.now()
    product.save()




    related_products = list(product.category.products.filter(parent = None).exclude(id = product.id))
    if len(related_products) >= 3:
        related_products = random.sample(related_products, 3)

    if product.parent:
        return redirect('product_detail', category_slug = category_slug, slug = product.parent.slug)

    imagesstring = "{'thumbnail': '%s', 'image': '%s'}," % (product.thumbnail.url, product.image.url)

    for image in product.images.all():
        imagesstring = imagesstring + ("{'thumbnail': '%s', 'image': '%s'}," % (image.thumbnail.url, image.image.url))

    cart = Cart(request)

    if cart.has_product(product.id):
        product.in_cart = True
    else:
        product.in_cart = False

    context = {
        'related_products':related_products,
        'product': product,
        'imagesstring': imagesstring
    }
    return render(request, 'product_detail.html', context) 

def category_detail(request,slug):
    category = get_object_or_404(Category, slug=slug)
    products = category.products.all()
    paginator = Paginator(products, 10)
    page_number = request.GET.get('page')
    
    page_obj = paginator.get_page(page_number)

    # Get the index of the current page
    index = page_obj.number - 1  # edited to something easier without index
    # This value is maximum index of your pages, so the last page - 1
    max_index = len(paginator.page_range)
    # You want a range of 7, so lets calculate where to slice the list
    start_index = index - 3 if index >= 3 else 0
    end_index = index + 3 if index <= max_index - 3 else max_index
    # Get our new page range. In the latest versions of Django page_range returns 
    # an iterator. Thus pass it to list, to make our slice possible again.
    page_range = list(paginator.page_range)[start_index:end_index]

   

    context = {
        'category': category,
        # 'count': book_paginator.count,
        'page_obj': page_obj,
        'page_range':page_range
        
    }

    return render(request, 'category_detail.html', context)