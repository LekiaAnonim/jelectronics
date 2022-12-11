from django.contrib import admin

# Register your models here.
from .models import Category, Vendor, Product, ProductInstance, PersonalDetails  # , Comment
from parler.admin import TranslatableAdmin

# from .models import Course

admin.site.register(Category, TranslatableAdmin)

# admin.site.register(Category)


# admin.site.register(ProductInstance)
admin.site.register(ProductInstance, TranslatableAdmin)
# @admin.register(ProductInstance)
class ProductInstanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'purchase_date', 'status', 'buyer')
    fields = ['id', 'product', 'buyer']
    list_filter = ('purchase_date',)


class ProductInstanceInline(admin.TabularInline):
    model = ProductInstance


# admin.site.register(Product)
admin.site.register(Product, TranslatableAdmin)

# @admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('model', 'category', 'vendor', 'price',
                    'discount_price', 'description', 'image', 'image2', 'image3', 'quantity_in_cart')
    fields = ['model', ('category', 'vendor'),
              ('price', 'discount_price'), 'description', 'image', 'image2', 'image3', 'quantity_in_cart']
    inlines = [ProductInstanceInline]


class ProductInline(admin.TabularInline):
    model = ProductAdmin

# admin.site.register(Vendor)
admin.site.register(Vendor, TranslatableAdmin)



class VendorAdmin(admin.ModelAdmin):
    list_display = ('name')
    inlines = [ProductInline, ProductInstanceInline]

# @admin.register(Comment)
# class CommentAdmin(admin.ModelAdmin):
#     list_display = ('name', 'body', 'product', 'created_on', 'active')
#     list_filter = ('active', 'created_on')
#     search_fields = ('name', 'body')
#     actions = ['approve_comments']

#     def approve_comments(self, request, queryset):
#         queryset.update(active = True)


admin.site.register(PersonalDetails, TranslatableAdmin)

# @admin.register(PersonalDetails)
class PersonalDetailsAdmin(admin.ModelAdmin):
    list_display = ('buyer', 'first_name', 'last_name', 'phone_number',
                    'address_line_1', 'address_line_2', 'country', 'state', 'city', 'zip_code', 'add_to_email_list')
    fields = [('buyer', 'first_name', 'last_name'), 'phone_number',
              ('address_line_1', 'address_line_2'), ('country', 'state', 'city', 'zip_code', 'add_to_email_list')]
