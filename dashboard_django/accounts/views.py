from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import *

def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()

    total_customers = customers.count()

    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    datas = {
        'orders': orders, 
        'customers': customers,
        'total_customers': total_customers,
        'total_orders': total_orders,
        'delivered': delivered,
        'pending': pending,
    }

    return render(request, 'accounts/dashboard.html', datas)

def products(request):
    products = Product.objects.all()
    return render(request, 'accounts/products.html', {'products': products})

def customer(request, pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()

    total_orders = orders.count()

    data = {'customer': customer, 'total_orders': total_orders, 'orders': orders}

    return render(request, 'accounts/customer.html', data)

def createOrder(request):
    form = OrderForm()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid:
            form.save() # Model form will handle the saving inside the database
            return redirect('/')

    data = {'form' : form}

    return render(request, 'accounts/order_form.html', data)

def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)

    data = {'form': form}

    return render(request, 'accounts/order_form.html', data)
