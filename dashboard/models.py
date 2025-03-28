from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=100, null=True)
    quantity = models.PositiveIntegerField(null=True)

    def __str__(self):
        return f'{self.name} (Quantity: {self.quantity})'

    def clean(self):
        if self.quantity < 0:
            raise ValidationError('Quantity cannot be negative.')


class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    staff = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    order_quantity = models.PositiveIntegerField(null=True)
    date = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.product is None:
            raise ValidationError('Product must be selected.')

        if self.product.quantity is None:
            raise ValidationError('Product quantity is not set.')

        if self.order_quantity is None:
            raise ValidationError('Order quantity must be specified.')

        if self.order_quantity > self.product.quantity:
            raise ValidationError('Order quantity cannot exceed available product quantity.')

    def __str__(self):
        return f'{self.product} ordered by {self.staff.username}'