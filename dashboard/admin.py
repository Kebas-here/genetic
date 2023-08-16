from django.contrib import admin
from .models import Product, Order
from django.contrib.auth.models import Group

admin.site.site_header= 'Dunia Ponselindo-Dashboard'

class ProductAdmin(admin.ModelAdmin):
    list_display = ('nama', 'kuantitas', 'kategori')
    list_filter = ('kategori',)

# Register your models here.
admin.site.register(Product, ProductAdmin)
admin.site.register(Order)
admin.site.unregister(Group)

