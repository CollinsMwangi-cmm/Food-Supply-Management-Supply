from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from .models import Product, Order
from .forms import ProductForm, OrderForm, ReportForm
from django.http import HttpResponse
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import base64
from io import BytesIO
import matplotlib
matplotlib.use('Agg')  # Use a non-GUI backend
import matplotlib.pyplot as plt



orders = Order.objects.all()
products = Product.objects.all()
users = User.objects.all()


def index(request):
    # Generate the product quantity chart
    product_names = [product.name for product in products]
    quantities = [product.quantity for product in products]

    # Create a bar chart
    plt.figure(figsize=(10, 6))
    plt.barh(product_names, quantities, color='skyblue')
    plt.xlabel('Quantity')
    plt.title('Product Quantities')
    plt.xlim(0, max(quantities) + 5)  # Add some space on the right
    plt.grid(axis='x')

    # Save the plot to a BytesIO object
    buf = BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)

    # Encode the image in base64
    chart_image = base64.b64encode(buf.getvalue()).decode('utf-8')  
    
    return render(request, 'dashboard/index.html',
                  {
                     'orders': orders, 
                     'users': users,
                     'products': products,
                     'chart_image': chart_image # Pass the chart image to the template
                  })


def staff_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the user
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']  # Use 'password1' instead of 'password'
            # Optionally log the user in after registration
            return redirect('dashboard-staff')  # Redirect to a success page
    else:
        form = UserCreationForm()
            
    return render(request, 'dashboard/staff.html',  {
        'users': users,
        'form':form,
        'products': products,
        'orders': orders
        
        })



def product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard-product')  # Redirect to the product dashboard after saving
    else:
        form = ProductForm()  # Create a new form instance for GET requests

    products = Product.objects.all()


    return render(request, 'dashboard/product.html', {
        'users': users,
        'products': products,
        'orders': orders,
        'form': form,
    })
    
def edit_product_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)  # Retrieve the product or return 404
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)  # Bind the form to the product instance
        if form.is_valid():
            form.save()  # Save the updated product
            return redirect('dashboard-product')  # Redirect to the product dashboard after saving
    else:
        form = ProductForm(instance=product)  # Create a form instance with the product data

    return render(request, 'dashboard/product_update.html', {
        'users': users,
        'products': products,
        'orders': orders,
        'form': form,
    })

def delete_product_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)  # Retrieve the product or return 404
    if request.method == 'POST':
        product.delete()  # Delete the product
        return redirect('dashboard-product')  # Redirect to the product dashboard after deletion

    return render(request, 'dashboard/product_delete.html', {
        'users': users,
        'products': products,
        'orders': orders,
    })

def order(request):
    orders = Order.objects.all()
    
    return render(request, 'dashboard/order.html', {
        'users': users,
        'products': products,
        'orders': orders
        })
    
    


def reports_view(request):
    report_html = None
    report_type = None

    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            report_type = form.cleaned_data['report_type']
            orders = get_orders(report_type)  
            report_html = render_to_string(f'dashboard/{report_type}_report.html', {'orders': orders})
    else:
        form = ReportForm()

    return render(request, 'dashboard/reports.html', {
        'form': form,
        'report_html': report_html,
        'report_type': report_type,
    })

def get_orders(report_type):
    now = timezone.now()
    if report_type == 'weekly':
        week_start = now - timezone.timedelta(days=7)
        return Order.objects.filter(date__gte=week_start)
    elif report_type == 'monthly':
        month_start = now.replace(day=1)
        return Order.objects.filter(date__gte=month_start)
    elif report_type == 'yearly':
        year_start = now.replace(month=1, day=1)
        return Order.objects.filter(date__gte=year_start)
    return Order.objects.none()

def generate_pdf_response(html_string, filename):
    from weasyprint import HTML  
    html = HTML(string=html_string)
    pdf = html.write_pdf()
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response

def download_report(request, report_type):
    orders = get_orders(report_type)
    html_string = render_to_string(f'dashboard/{report_type}_report.html', {'orders': orders})
    return generate_pdf_response(html_string, f'{report_type}_report.pdf')