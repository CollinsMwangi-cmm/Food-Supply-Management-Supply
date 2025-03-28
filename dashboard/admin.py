from django.contrib import admin
from .models import Product, Order
from django.contrib.auth.models import Group

admin.site.site_header = 'Freshstock Food Supply'

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'quantity')
    

# Register your models here.
admin.site.register(Product, ProductAdmin)
admin.site.register(Order)
#admin.site.unregister(Group)

