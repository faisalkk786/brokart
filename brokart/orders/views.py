from django.shortcuts import render, redirect
from . models import Order, OrderedItem, Product
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
def show_cart(request):
    user=request.user
    customer=user.customer_profile
    cart_obj=Order.objects.filter(
            owner=customer,
            order_status=Order.CART_STAGE
    ).first()

    context={'cart':cart_obj}
    return render(request, 'cart.html', context)

@login_required(login_url='account')
def add_to_cart(request):
    if request.POST:
        user=request.user
        customer=user.customer_profile
        quantity=int(request.POST.get('quantity'))
        product_id=request.POST.get('product_id')
        product_obj=Product.objects.get(id=product_id)
        # get or create the order with this loggin customer and cart_stage=0, returning result will be a tuple
        cart_obj,created=Order.objects.get_or_create(
            owner=customer,
            order_status=Order.CART_STAGE
        )
        ordered_item,created=OrderedItem.objects.get_or_create(
            product=product_obj,
            owner=cart_obj
        )
        if created:
            ordered_item.quantity=quantity
            ordered_item.save()
        else:
            ordered_item.quantity=ordered_item.quantity+quantity
            ordered_item.save()
        return redirect('cart')

def remove_item_from_cart(request,pk):
    item=OrderedItem.objects.get(pk=pk)
    if item:
        item.delete()
    return redirect('cart')

def checkout_cart(request):
    if request.POST:
        try:
            user=request.user
            customer=user.customer_profile
            #passing total from form
            total=float(request.POST.get('total'))
            order_obj=Order.objects.get(
                owner=customer,
                order_status=Order.CART_STAGE
            )
            if order_obj:
                order_obj.total_price=total
                order_obj.order_status=Order.ORDER_CONFIRMED
                order_obj.save()
                status_message="Your Order is Processed. Your Item will be delivered Shortly"
                messages.success(request, status_message)
            else:
                status_message="Unable to Process. No item in Cart"
                messages.error(request, status_message)
        except Exception as e:
            status_message="Unable to Process. No item in Cart"
            messages.error(request, status_message)
    return redirect('cart')
        

@login_required(login_url='account')
def view_orders(request):
    user=request.user
    customer=user.customer_profile
    all_orders_obj=Order.objects.filter(owner=customer).exclude(order_status=Order.CART_STAGE)
    context={'orders':all_orders_obj}
    return render(request, 'orders.html', context)