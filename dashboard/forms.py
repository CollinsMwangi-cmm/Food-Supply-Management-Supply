from django import forms
from .models import Product, Order

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'quantity']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter product name'}),
            'quantity': forms.NumberInput(attrs={'placeholder': 'Enter quantity'}),
        }

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity is not None and quantity < 0:
            raise forms.ValidationError('Quantity cannot be negative.')
        return quantity


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['product', 'order_quantity']  # Exclude 'staff' from the form
        widgets = {
            'product': forms.Select(attrs={'class': 'form-control'}),
            'order_quantity': forms.NumberInput(attrs={'placeholder': 'Enter order quantity'}),
        }

    def clean_order_quantity(self):
        order_quantity = self.cleaned_data.get('order_quantity')
        product = self.cleaned_data.get('product')

        if product:
            # Get the product instance
            product_instance = Product.objects.get(id=product.id)
            if order_quantity > product_instance.quantity:
                raise forms.ValidationError('Order quantity cannot exceed available product quantity.')
        
        return order_quantity

    def clean(self):
        cleaned_data = super().clean()
        product = cleaned_data.get('product')
        order_quantity = cleaned_data.get('order_quantity')

        if product and order_quantity:
            product_instance = Product.objects.get(id=product.id)
            if order_quantity > product_instance.quantity:
                self.add_error('order_quantity', 'Order quantity cannot exceed available product quantity.')

        return cleaned_data
    
class ReportForm(forms.Form):
    REPORT_CHOICES = [
        ('weekly', 'Weekly Report'),
        ('monthly', 'Monthly Report'),
        ('yearly', 'Yearly Report'),
    ]
    report_type = forms.ChoiceField(choices=REPORT_CHOICES)