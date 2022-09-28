from contextlib import _RedirectStream
from django.shortcuts import render, redirect
from application1.form import CustomUserForm
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
import json
from django.http import JsonResponse,HttpResponseBadRequest

################### Home Page ###############################
def Home(request):
    homeproducut= Product.objects.filter(trending=1)
    return render(request,"temp1/index.html",{"homeproducut":homeproducut})

#################### User Register page #########################
def Register(request):
    form=CustomUserForm()
    if request.method=='POST':
        form=CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request,'User Account Created Sucessfully')
    return render(request,"temp1/register.html",{"form":form})

################## Login Page #################################    
def Login(request):
    if request.user.is_authenticated:
        return redirect("/")
    else:
        if request.method=='POST':
            name=request.POST.get('username')
            pwd=request.POST.get('password')
            user=authenticate(request,username=name,password=pwd)
            if user is not None:
                login(request,user)
                messages.success(request,"Logged in sucessfully")
                return redirect("/")
            else:
                messages.error(request,"Invalid User Name or Password")
                return redirect("login/")
        return render(request,"temp1/login.html")

################### Logout Page ##################################
def Log_out(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request,"Logged Out Sucessfully")
    return redirect("/")

################### Product Collection Page ######################    
def Collections(request):
    separate= Catagory.objects.filter(status=0)
    return render(request,"temp1/collection.html",{"separate":separate})

######################product view page -1#####################
def Collections_view(request,name):
    if(Catagory.objects.filter(name=name,status=0)):
        pro=Product.objects.filter(category__name=name)
        return render(request,"produtes/ind.html",{"pro":pro,"category":name})
    else:
        messages.warning(request,"No Such Catagory Found")
        return _RedirectStream('collection')

##################### product view page-2##########################
def Product_details(request,cname,pname):
    if(Catagory.objects.filter(name=cname,status=0)):
        if(Product.objects.filter(name=pname,status=0)):
            tyjh=Product.objects.filter(name=pname,status=0).first()
            return render(request,"produtes/product_details.html",{"pd":tyjh})
        else:
            messages.error(request,"No Such Catagory Found")
            return _RedirectStream('collection')
    else:
        messages.error(request,"No Such Catagory Found")
        return _RedirectStream('collection')

#################Add_to_cart page#################################

def Add_to_cart(request):
    #User=request.User.id
    if request.headers.get('X-Requested-With')=='XMLHttpRequest':
        if request.user.is_authenticated:
            data=json.load(request)
            product_qty=data['product_qty']
            product_id=data['pid']
            product_status=Product.objects.get(id=product_id)
            if product_status:
                 if Cart.objects.filter(user=request.user.id,product_id=product_id):
                     return JsonResponse({'status':'Product Already in Cart'},status=200)
                 else:
                     if product_status.quantity>=product_qty:
                         Cart.objects.create(user=request.user,product_id=product_id,product_qty=product_qty)
                         return JsonResponse({'status':'Product Added to Cart'},status=200)
                     else:
                         return JsonResponse({'status':'Product Stock Not Available'},status=200)
        else:
            return JsonResponse({'status':'Login to Add Cart'},status=200)
    else:
        return JsonResponse({'status':'Invalid Access'},status=200) 

###########################Cart page##############################

def Cart_page(request):
    if request.user.is_authenticated:
        cart=Cart.objects.filter(user=request.user)
        return render(request,"temp1/cartpage.html",{"cart":cart})
    else:
        return redirect("temp1/cartpage.html")

#################################Remove_Cart###############################


        



