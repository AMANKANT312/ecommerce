from django.shortcuts import render , redirect
from django.views import View
from .models import *
from .forms import CustomerRegistrationForm ,CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse

# def home(request):
#  return render(request, 'app/home.html')
class Productview(View):
 def get(self,request):
  topwears = Product.objects.filter(category = "TW")
  bottomwears = Product.objects.filter(category = "BW")
  mobiles = Product.objects.filter(category = "M")
  return render( request, 'app/home.html',{'topwears':topwears,'bottomwears':bottomwears,'mobiles':mobiles})
 

def product_detail(request,pk):
 product = Product.objects.get(pk=pk)
 productincart = False
 productincart=Cart.objects.filter(Q(user=request.user) & Q(product=product)).exists()
 print(productincart)
 return render(request, 'app/productdetail.html' ,{'product':product,'productexist':productincart})

def add_to_cart(request):
 if request.method=='POST':
  usr = request.user
  print(usr)
  productid =request.POST['product_id']
  # product=Product.objects.filter(id=productid).first()
  product = Product.objects.get(id=productid)
  print(productid)
  cart = Cart.objects.create(user=usr,product=product)
  cart.save()
  print (cart)
  return redirect ("/cart")
#   cartdata = Cart.objects.filter(user=usr)
#   print(cartdata)
#   return render(request, 'app/addtocart.html', {'data':cartdata})
#  else :
#   if request.user.is_authenticated:
#    usr=request.user
#    cartdata = Cart.objects.filter(user=usr)
#    return render(request, 'app/addtocart.html', {'data':cartdata})
   
def show_cart (request):
 if request.user.is_authenticated:
    usr=request.user
    cartdata = Cart.objects.filter(user=usr)
    cart = Cart.objects.all()
    datas = []

    cartdata = Cart.objects.filter(user=usr)
    if cartdata:
      datas.append(cartdata)
  
    print(datas)
    if datas :
       for products in datas:
        temp = 0.0
        shiping = 70.0
        for p in products:
         price=  (p.quantity * p.product.discounted_price)
        # print(type(price))
         temp = temp+price
        # print(temp)
        total = temp
        total_amnt = temp + shiping
       return render(request, 'app/addtocart.html', {'data':cartdata , 'amount':total, 'total':total_amnt})
    else:
     return render(request, 'app/emptycart.html')
     
def plus_cart(request):
 if request.method == 'GET':
  prod_id = request.GET['prod_id']
  print(prod_id)
  c = Cart.objects.get(Q(product =prod_id) & Q(user=request.user))
  c.quantity+=1
  c.save()
  datas = []

  cartdata = Cart.objects.filter(user=request.user)
  if cartdata:
      datas.append(cartdata)
  
  print(datas)
  if datas :
       for products in datas:
        temp = 0.0
        shiping = 70.0
        for p in products:
         price=  (p.quantity * p.product.discounted_price)
        # print(type(price))
         temp = temp+price
        # print(temp)
        total = temp
        total_amnt = temp + shiping
  data = {'quantity': c.quantity,'amount':total,'totalamount':total_amnt }
  return JsonResponse(data)
  
def minus_cart(request):
 if request.method == 'GET':
  prod_id = request.GET['prod_id']
  print(prod_id)
  c = Cart.objects.get(Q(product =prod_id) & Q(user=request.user))
  c.quantity-=1
  c.save()
  datas = []

  cartdata = Cart.objects.filter(user=request.user)
  if cartdata:
      datas.append(cartdata)
  
  print(datas)
  if datas :
       for products in datas:
        temp = 0.0
        shiping = 70.0
        for p in products:
         price=  (p.quantity * p.product.discounted_price)
        # print(type(price))
         temp = temp+price
        # print(temp)
        total = temp
        total_amnt = temp + shiping
  data = {'quantity': c.quantity,'amount':total,'totalamount':total_amnt }
  return JsonResponse(data)
 
def remove_item(request):
 if request.method == 'GET':
  prod_id = request.GET['prod_id']
  # print(prod_id)
  c = Cart.objects.get(Q(product =prod_id) & Q(user=request.user))
  c.delete()
  datas = []
  temp = 0.0
  shiping = 70.0
  cartdata = Cart.objects.filter(user=request.user)
  if cartdata:
      datas.append(cartdata)
  
  # print(datas)
  if datas :
       for products in datas:
        # temp = 0.0
        # shiping = 70.0
        for p in products:
         price=  (p.quantity * p.product.discounted_price)
        # print(type(price))
         temp = temp+price
        # print(temp)
      
  total_amnt = temp + shiping
 data = {'amount':temp,'totalamount':total_amnt }
 return JsonResponse(data)


def buy_now(request):
 return render(request, 'app/buynow.html')

# def profile(request):
#  return render(request, 'app/profile.html')

def address(request):
 add = Customer.objects.filter(user = request.user)
 return render(request, 'app/address.html',{'add':add})

def orders(request):
 usr = request.user
 if request.method=='POST':
   custid=request.POST["address"]
   customer=Customer.objects.get(id=custid)
 cart = Cart.objects.filter(user=usr) 
 for c in cart:
   Orderplace(user=usr,customer=customer,product=c.product,quantity=c.quantity).save()
   c.delete()
 op= Orderplace.objects.filter(user=usr)
 return render(request, 'app/orders.html',{'ordered':op})
 
def change_password(request):
 return render(request, 'app/changepassword.html')

def mobile(request, data=None):
 if data == None:
   mobiles = Product.objects.filter(category = 'M')
 elif data == "redmi" or data == 'samsung':
   mobiles = Product.objects.filter(category = 'M').filter(brand=data)
 elif data == 'below':
   mobiles = Product.objects.filter(category = 'M').filter(discounted_price__lt = 10000)
 elif data == 'above':
    mobiles = Product.objects.filter(category = 'M').filter(discounted_price__gt = 10000)
 return render(request, 'app/mobile.html' , {'mobiles':mobiles})

# def login(request):
 
#  return render(request, 'app/login.html')

# def customerregistration(request):
   
#         return render (request,'app/customerregistration.html')
class CustomerRegistrationView(View):
 def get(self,request):
  form = CustomerRegistrationForm()
  return render(request,'app/customerregistration.html',{'form':form})
 def post (self,request):
  form = CustomerRegistrationForm(request.POST)
  if form.is_valid():
   messages.success(request, 'Congratulations registered suceesfully')
   form.save()
   return render(request,'app/customerregistration.html',{'form':form})
  else:
   return render(request,'app/customerregistration.html',{'form':form})
    
  # return render(request, 'app/customerregistration.html')

def checkout(request):
 user = request.user
 address = Customer.objects.filter(user=user)
 print(address)
 cartitem = Cart.objects.filter(user=user)

 return render(request, 'app/checkout.html',{'address':address ,'cartitem':cartitem})

class ProfileView(View):
 def get(self, request):
  form = CustomerProfileForm()
  return render( request, 'app/profile.html',{'form':form, 'active':"btn-secondary"})
 def post(self,request):
  form = CustomerProfileForm(request.POST)
  if form.is_valid():
   usr = request.user
   name = form.cleaned_data['name']
   locality = form.cleaned_data['locality']
   city = form.cleaned_data['city']
   state = form.cleaned_data['state']
   zipcode = form.cleaned_data['zipcode']
   reg = Customer(user = usr,name=name,locality=locality,state=state,city=city,zipcode=zipcode)
   reg.save()
   messages.success(request, 'congratulations ')
  return render (request,'app/profile.html',{'form':form,'active':'btn-primary'})

