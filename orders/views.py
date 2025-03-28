from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction  # Import transaction for atomic operations
from dashboard.models import Order, Product
from dashboard.forms import OrderForm

@login_required
def overview(request):
    orders = Order.objects.filter(staff=request.user) 
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)  # Create an Order instance but don't save yet
            order.staff = request.user  # Set the logged-in user as the staff
            
            # Use a transaction to ensure atomicity
            with transaction.atomic():
                product = form.cleaned_data['product']  # Get the product from the form
                order_quantity = form.cleaned_data['order_quantity']  # Get the order quantity
                
                # Reduce the product quantity
                product.quantity -= order_quantity
                product.save()  # Save the updated product quantity
                
                order.save()  # Now save the Order instance
            
            return redirect('overview')  # Redirect to an order list view
    else:
        form = OrderForm()
    return render(request, 'orders/overview.html', {'orders': orders, 'form': form})