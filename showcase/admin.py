from django.contrib import admin

# Register your models here.
from .models import Category, Vendor, Product, ProductInstance

admin.site.register(Category)


# admin.site.register(ProductInstance)
@admin.register(ProductInstance)
class ProductInstanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'image', 'purchase_date', 'status', 'buyer')
    fields = ['id', 'product', 'image', 'status', 'buyer']
    list_filter = ('purchase_date', 'status')

class ProductInstanceInline(admin.TabularInline):
    model = ProductInstance

# admin.site.register(Product)
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('model', 'category', 'vendor', 'price', 'discount_price', 'description', 'image')
    fields = ['model', ('category', 'vendor'),
              ('price', 'discount_price'), 'description', 'image']
    inlines = [ProductInstanceInline]

admin.site.register(Vendor)
class ProductInline(admin.TabularInline):
    model = ProductAdmin


class VendorAdmin(admin.ModelAdmin):
    list_display = ('name')
    inlines = [ProductInline, ProductInstanceInline]
