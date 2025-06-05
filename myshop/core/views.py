from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from django.db.models import Count
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
# Create your views here.
def index(request):
    offer=offerProduct.objects.all()



    cate=Category.objects.all()

    cateid=request.GET.get('category')
    brid=request.GET.get('brand')
    if cateid and brid:
        product=Product.objects.filter(subcategory=cateid,brand=brid)
    elif cateid:
        product=Product.objects.filter(subcategory=cateid)
    else:
         product=Product.objects.all()
    br=Brand.objects.annotate(product_count=Count('product'))

    paginator=Paginator(product,1)
    num_p=request.GET.get('page')
    data=paginator.get_page(num_p)
    total=data.paginator.num_pages
    context={
        'offer':offer,
        'product':product,
        'cate':cate,
        'br':br,
        'data':data,
        'num':[i+1 for i in range(total)]
    }
    return render(request,'core/index.html',context)

def prooduct_detail(request,id):
    data=get_object_or_404(Product,id=id)
    return render(request,'core/prooduct_detail.html',{'data':data})

#      add to card

@login_required(login_url="log_in")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("index")


@login_required(login_url="log_in")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url="/log_in")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="log_in")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required(login_url="log_in")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required(login_url="log_in")
def cart_detail(request):
  return render(request, 'core/cart.html')