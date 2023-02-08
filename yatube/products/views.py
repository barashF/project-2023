from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Basket, Order, ImgProduct, Category, Subcategory, Brand
from .forms import ProductForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from datetime import datetime
import simplejson as json
from django.db.models import Q

User = get_user_model()

def main_page_market(request):
    slots = Product.objects.order_by("-pub_date").all()
    categories = Category.objects.all()
    basket = Basket.objects.filter(user=request.user)
    products = []
    for i in basket:
        products.append(i.product)
    return render(request, "main_page.html", {'categories':categories, 'slots':slots})

def check_basket(request):
    basket = Basket.objects.filter(user=request.user)
    products = []
    for i in basket:
        products.append(i.product.id)
    return JsonResponse({'products':products})
    
def new_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST or None)
        if form.is_valid():
            new_product = form.save(commit=False)
            new_product.seller = request.user
            new_product.save()
    form = ProductForm()
    return render(request, "new_product.html", {"form": form})

def add_product_basket(request):
    user = request.user
    product_id = request.POST['product_id']
    product = get_object_or_404(Product, pk=product_id)
    basket_check = Basket.objects.filter(user=user, product=product).count()
    if basket_check == 0:
        Basket.objects.create(product=product, user=user, pub_date=datetime.now)
    return redirect("basket")

def basket_delete(request):
    basket_id = request.POST.get('basket_id')
    basket = get_object_or_404(Basket, pk=basket_id)
    Basket.objects.filter(user=request.user, product=basket.product).delete()

@login_required
def page_basket(request):
    basket = Basket.objects.filter(user=request.user).order_by("-pub_date").all()
    categories = Category.objects.all()
    return render(request, "basket.html", {"basket": basket, "categories":categories})

@login_required
def profile(request, username):
    profile = get_object_or_404(User, username=username)
    user = request.user
    categories = Category.objects.all()
    data = {
        'profile':profile,
        'user':user,
        'categories':categories
    }
    return render(request, 'profile.html', data)

def new_order(request, basket_id):
    basket = get_object_or_404(Basket, pk=basket_id)
    product = get_object_or_404(Product, pk=basket.product.id)
    product.price = int(product.price)
    categories = Category.objects.all()
    return render(request, 'new_order.html', {'product':product, 'categories':categories})

def product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    categories = Category.objects.all()
    description = product.description.split('!')
    descriptions = []
    for i in description:
        descriptions.append(i)
    images = ImgProduct.objects.filter(product=product)
    return render(request, 'product.html', {'product':product, 'images': images, 'descriptions':descriptions, 'categories':categories})

def subcategory(request, category_id):
    categories = Category.objects.all()
    category = get_object_or_404(Category, pk=category_id)
    subcategories = Subcategory.objects.filter(category=category)
    return render(request, 'subcategory.html', {"subcategories":subcategories, "categories":categories})

def search(request):
    categories = Category.objects.all()
    text_search = request.GET.get('search', '')
    brands = Brand.objects.all()
    if text_search:
        q_list = Q()
        for word in text_search.split():
            q_list |= Q(name__iregex = word)
            q_list |= Q(description__iregex = word)
        products = Product.objects.filter(q_list)
        return render(request, 'search_page.html', {"categories":categories, 'text_search':text_search, 'products':products, 'brands':brands})
    else:
        return redirect('market')