from django.http import request
from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect,get_object_or_404
from .models import *
import json
import datetime
from django.http import JsonResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm,CommentForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from .decorators import allowed_users,unauthenticated_user
from django.contrib.auth.models import User

def index(request):
	context = {}
	return render(request,'store/index.html',context)

def index2(request):
	context = {}
	return render(request,'store/index2.html',context)

@allowed_users(['admin'])
def staffHome(request):
	context = {}
	return render(request,'store/staffhome.html',context)

def detailPage(request,id):
	product = Product.objects.get(id=id)
	
	customer = request.user.customer
	order , created = Order.objects.get_or_create(customer=customer,complete=False)
	items = order.orderitem_set.all()
	cartItems= order.get_cart_items
	form = CommentForm()
	if request.method == 'POST':
		form = CommentForm(request.POST,author=request.user,product=product)
		if form.is_valid():
			form.save()
		return HttpResponseRedirect(request.path)
	context = {'product' : product,'cartItems':cartItems ,'form':form }
	return render(request,'store/details.html',context)



def store(request):

	if request.user.is_authenticated:
		customer = request.user.customer
		order , created = Order.objects.get_or_create(customer=customer,complete=False)
		items = order.orderitem_set.all()
		cartItems= order.get_cart_items
	else:
		items = []
		order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
		cartItems = order['get_cart_items']

	products = Product.objects.all()
	context = {'products':products,'cartItems':cartItems}
	return render(request, 'store/store.html', context)

def cart(request):
	if request.user.is_authenticated:
		customer = request.user.customer
		order , created = Order.objects.get_or_create(customer=customer,complete=False)
		items = order.orderitem_set.all()
		cartItems= order.get_cart_items
	else:
		items = []
		order = {'get_cart_total':0, 'get_cart_items':0}
		cartItems= order.get_cart_items
	context = {'items':items,'order':order,'cartItems':cartItems}
	return render(request, 'store/cart.html', context)
	

def checkout(request):
	#login user
	if request.user.is_authenticated:
		customer = request.user.customer
		order , created = Order.objects.get_or_create(customer=customer,complete=False)
		items = order.orderitem_set.all()
		cartItems= order.get_cart_items
	else:
		# guest
		items = []
		order = {'get_cart_total':0, 'get_cart_items':0}
		cartItems= order.get_cart_items
	context = {'items':items,'order':order,'cartItems':cartItems,'shipping':False}
	return render(request, 'store/checkout.html', context)


def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)

	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)


def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
	else:
		print("User is not logged in")

	total = float(data['form']['total'])
	order.transaction_id = transaction_id

	if total == order.get_cart_total:
		order.complete = True
	order.save()

	if order.shipping == True:
		ShippingAddress.objects.create(
		customer=customer,
		order=order,
		address=data['shipping']['address'],
		city=data['shipping']['city'],
		district=data['shipping']['district'],
		zipcode=data['shipping']['zipcode'],
		)

	return JsonResponse('Payment submitted..', safe=False)

@unauthenticated_user
def registerPage(request):
	form = CreateUserForm()
	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			form.save()
			user = form.cleaned_data.get('username')
			messages.success(request, 'Đăng ký tài khoản thành công')

			return redirect('login')
			

	context = {'form':form}
	return render(request, 'store/register.html', context)

@unauthenticated_user
def loginPage(request):
	
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			return redirect('store')
		else:
			messages.info(request, 'Tài khoản hoặc mật khẩu không chính xác')

	context = {}
	return render(request, 'store/login.html', context)


def logoutUser(request):
	logout(request)
	return redirect('index2')





