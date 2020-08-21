from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
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

# TODO I NEED TO CHECK OUT THIS AGAIN .. 
def createOrder(request, pk):
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
    order = Order.objects.get(id=pk)

    if request.method == "POST":
        order.delete()
        return redirect('/')

    data = {'item': order}

    return render(request, 'accounts/delete.html', data)
