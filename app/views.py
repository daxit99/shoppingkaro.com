from django.contrib.auth.models import User
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.views import View
from .models import Customer,Product,Cart,OrderPlaced
from .forms import CustomerRegistrationForm,CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from app import forms

class ProductView(View):
    def get(self,request):
        totalitem=0
        topwears=Product.objects.filter(category='TW')
        bottomwears=Product.objects.filter(category='BW')
        mobiles=Product.objects.filter(category='M')
        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))
        return render(request, 'app/home.html',{'topwears':topwears,'bottomwears':bottomwears,'mobiles':mobiles,'totalitem':totalitem})


class ProductDeatilView(View):
    def get(self,request,pk):
        totalitem=0
        product = Product.objects.get(pk=pk)
        
        item_already_in_cart=False
        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))
            item_already_in_cart=Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
        return render(request, 'app/productdetail.html',{'product':product,'item_already_in_cart':item_already_in_cart,'totalitem':totalitem})
        
@login_required
def add_to_cart(request):
    user=request.user
    product_id=request.GET.get('prod_id')
    product=Product.objects.get(id=product_id)
    Cart(user=user,product=product).save()
    return redirect('/cart')

@login_required
def show_cart(request):
    totalitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
        user=request.user
        cart=Cart.objects.filter(user=user)
        print(cart)
        amount=0.0
        shipping_amount=70.0
        total_amount=0.0
        cart_product=[p for p in Cart.objects.all() if p.user == user]
        # print(cart_product)
        if cart_product:
            for p in cart_product:
                tempamount=(p.quantity * p.product.discount_price)
                amount += tempamount
                totalamount=amount + shipping_amount
            return render(request, 'app/addtocart.html',
            {'carts':cart,'totalamount':totalamount,'amount':amount,'totalitem':totalitem})
        else:
            return render(request,'app/emptycart.html',)

def plus_cart(request):
    if request.method=='GET':
        prod_id=request.GET['prod_id']
        print(prod_id)
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        amount=0.0
        shipping_amount=70.0
        cart_product=[p for p in Cart.objects.all() if p.user == request.user]
    for p in cart_product:
        tempamount=(p.quantity * p.product.discount_price)
        amount += tempamount

    data={
        'quantity': c.quantity,
        'amount': amount,
        'totalamount':amount + shipping_amount
        }
    return JsonResponse(data)

def minus_cart(request):
    if request.method=='GET':
        prod_id=request.GET['prod_id']
        print(prod_id)
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        amount=0.0
        shipping_amount=70.0
        cart_product=[p for p in Cart.objects.all() if p.user == request.user]
    for p in cart_product:
        tempamount=(p.quantity * p.product.discount_price)
        amount += tempamount

    data={
        'quantity': c.quantity,
        'amount': amount,
        'totalamount':amount + shipping_amount
        }
    return JsonResponse(data)

def remove_cart(request):
    if request.method=='GET':
        prod_id=request.GET['prod_id']
        print(prod_id)
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        amount=0.0
        shipping_amount=70.0
        cart_product=[p for p in Cart.objects.all() if p.user == request.user]
    for p in cart_product:
        tempamount=(p.quantity * p.product.discount_price)
        amount += tempamount

    data={
        'amount': amount,
        'totalamount':amount + shipping_amount
        }
    return JsonResponse(data)

def buy_now(request):
 return render(request, 'app/buynow.html')


@login_required
def address(request):
    totalitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
        add=Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html',{'add':add,'active':'btn-primary','totalitem':totalitem})


@login_required
def orders(request):
    totalitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
        op= OrderPlaced.objects.filter(user=request.user)   
    return render(request, 'app/orders.html',{'order_placed':op,'totalitem':totalitem})


def mobile(request,data=None):
    totalitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
    if data==None:
        mobile=Product.objects.filter(category='M')
    elif data == 'apple' or data == 'Vivo':
        mobile=Product.objects.filter(category='M').filter(brand=data)
    elif data=='below':
        mobile=Product.objects.filter(category='M').filter(discount_price__lt=20000)
    elif data=='above':
        mobile=Product.objects.filter(category='M').filter(discount_price__gt=20000)
    return render(request, 'app/mobile.html',{'mobile':mobile,'totalitem':totalitem})

def topwear(request,data=None):
    totalitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
    if data==None:
        topwear=Product.objects.filter(category='TW')
    elif data == 'levis' or data == 'Nike':
        topwear=Product.objects.filter(category='TW').filter(brand=data)
    elif data=='below':
        topwear=Product.objects.filter(category='TW').filter(discount_price__lt=1000)
    elif data=='above':
        topwear=Product.objects.filter(category='TW').filter(discount_price__gt=1000)
    return render(request, 'app/topwear.html',{'topwear':topwear,'totalitem':totalitem})


def bottomwear(request,data=None):
    totalitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
    if data==None:
        bottomwear=Product.objects.filter(category='BW')
    elif data == 'addidas' or data == 'Diesel':
        bottomwear=Product.objects.filter(category='BW').filter(brand=data)
    elif data=='below':
        bottomwear=Product.objects.filter(category='BW').filter(discount_price__lt=700)
    elif data=='above':
        bottomwear=Product.objects.filter(category='BW').filter(discount_price__gt=700)
    return render(request, 'app/bottomwear.html',{'bottomwear':bottomwear,'totalitem':totalitem})

def laptop(request,data=None):
    totalitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
    if data==None:
        laptop=Product.objects.filter(category='L')
    elif data == 'apple' or data == 'HP':
        laptop=Product.objects.filter(category='L').filter(brand=data)
    elif data=='below':
        laptop=Product.objects.filter(category='L').filter(discount_price__lt=30000)
    elif data=='above':
        laptop=Product.objects.filter(category='L').filter(discount_price__gt=30000)
    return render(request, 'app/laptop.html',{'laptop':laptop,'totalitem':totalitem})

    

def login(request):
 return render(request, 'app/login.html')

# def customerregistration(request):
#  return render(request, 'app/customerregistration.html')

class CustomerRegistrationView(View):
    def get(self,request):
        form=CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html',{'form':form})
    def post(self,request):
        form=CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request,'Congratulation!! Registered Successfully')
            form.save()
        return render(request, 'app/customerregistration.html',{'form':form})



@login_required
def checkout(request):
    totalitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
    user=request.user
    add=Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    amount=0.0
    shipping_amount=70.0
    totalamount=0.0
    cart_product=[p for p in Cart.objects.all() if p.user == request.user]
    if cart_product:
        for p in cart_product:
            tempamount=(p.quantity * p.product.discount_price)
            amount += tempamount 
        totalamount=amount+shipping_amount
    return render(request, 'app/checkout.html', {'add':add,'totalamount':totalamount,'cart_items':cart_items,'totalitem':totalitem})

@login_required
def payment_done(request):
    totalitem=0
    user=request.user
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
    custid=request.GET.get('custid')
    customer=Customer.objects.get(id=custid)
    cart=Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user,customer=customer,product=c.product,quantity=c.quantity).save()
        c.delete()
    return redirect("orders")

@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self,request):
        totalitem=0
        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))
            form=CustomerProfileForm()
        return render(request,'app/profile.html',{'form':form,'active':'btn-primary','totalitem':totalitem})


    def post(self,request):
        form=CustomerProfileForm(request.POST)
        if form.is_valid():
            usr= request.user
            name=form.cleaned_data['name']
            locality=form.cleaned_data['locality']
            city=form.cleaned_data['city']
            state=form.cleaned_data['state']
            zipcode=form.cleaned_data['zipcode']   

            reg=Customer(user=usr,name=name,locality=locality,city=city,state=state,zipcode=zipcode)
            reg.save()
            messages.success(request,'Congratulation!! profile Updated Successfully')
        return render(request,'app/profile.html',{'form':form,'active':'btn-primary'})


