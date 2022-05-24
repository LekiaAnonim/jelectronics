from django import forms
from .models import Category, Vendor, Product, ProductInstance
from . import views

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class AddToCart(forms.Form):
    quantity = forms.IntegerField(initial="1")

    def clean_quantity(self):
        data = self.cleaned_data['quantity']
        
        # check if amount added to cart is not greater than available quantity.
        if data > product.productinstance_set.all.count():
            raise ValidationError(('This quantity of' + str(product.model) + 'is not available at the moment'))
        
        # Remember to always return the cleaned data.
        return data
