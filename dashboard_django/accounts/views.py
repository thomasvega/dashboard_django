from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from django.contrib.auth.decorators import login_required

from .models import *
from .forms import OrderForm, CreateUserForm
from .filters import OrderFilter
from .decorators import unauthenticated_user

"""
    This file will contain methods with intelligence 
    that will render a template with or without data.

    Those methods can be connected with the database
"""


def registerPage(request):
    """
        This method will permit the use to register to the app
        We created a specific class to change default registration of django
        called CreateUserForm()
    """
    # Bad way to do this, but it permit us to understand how it works
    if request.user.is_authenticated:
        return redirect('home')

    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + user)
            return redirect('login')

    context = {'form': form}
    return render(request, 'accounts/register.html', context)

@unauthenticated_user
def loginPage(request):
    """
        Login method to authenticate the user
        It use modules of django
    """
    
    if request.user.is_authenticated:
        return redirect('home')# Bad way to do this, but it permit us to understand how it works

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username OR password is incorrect')

    context = {}
    return render(request, 'accounts/login.html', context)

def logoutUser(request):
    """
        Logout the user using the logout method from django
    """
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def home(request):
    """
    Protected route with decorator login_required. The user will be redirected if the user isn't connected
    """
    orders = Order.objects.all()
    customers = Customer.objects.all()

    total_customers = customers.count()

    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    datas = { 'orders': orders, 'customers': customers, 'total_customers': total_customers, 'total_orders': total_orders, 'delivered': delivered, 'pending': pending, }

    return render(request, 'accounts/dashboard.html', datas)


def userPage(request):
    context = {}
    return render(request, 'accounts/user.html', context)


def products(request):
    """
    Retrieving all products
    """
    products = Product.objects.all()
    return render(request, 'accounts/products.html', {'products': products})


def customer(request, pk):
    """
    Retrieving all customer with total orders, orders and order filter 
    """
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()
    total_orders = orders.count()
    order_filter = OrderFilter(request.GET, queryset=orders)
    orders = order_filter.qs
    data = { 'customer': customer, 'total_orders': total_orders, 'orders': orders, 'order_filter': order_filter, }
    return render(request, 'accounts/customer.html', data)


# TODO I NEED TO CHECK OUT THIS AGAIN .. 
def createOrder(request, pk):
    """
    Creating an order by getting the customer id from primary key
    """
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status')) # Need to gives the parent and child model
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(instance=customer)
    #form = OrderForm(initial={'customer': customer})
    if request.method == 'POST':
        #form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST, instance=customer)
        if form.is_valid:
            formset.save() # Model form will handle the saving inside the database
            return redirect('/')

    data = {'formset' : formset}

    return render(request, 'accounts/order_form.html', data)


def updateOrder(request, pk):
    """
    Updating the order with django URL using post method and passing the primary key
    """
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order) # adding instance to make sure it will not create a new one but will update
        if form.is_valid:
            form.save() # Model form will handle the saving inside the database
            return redirect('/')
    data = {'form': form}

    return render(request, 'accounts/order_form.html', data)


def deleteOrder(request, pk):
    """
        Deleting order with django orm
        Passing the primary key to be able to delete it
    """
    order = Order.objects.get(id=pk)

    if request.method == "POST":
        order.delete()
        return redirect('/')

    data = {'item': order}

    return render(request, 'accounts/delete.html', data)

