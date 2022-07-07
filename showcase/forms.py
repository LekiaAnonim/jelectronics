from django import forms
from .models import Category, Vendor, Product, ProductInstance, Comment
from . import views

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.forms import ModelForm, TextInput, EmailInput, Textarea


class AddToCart(forms.Form):
    quantity = forms.IntegerField(initial="1")

    def clean_quantity(self):
        data = self.cleaned_data['quantity']

        # check if amount added to cart is not greater than available quantity.
        if data > product.productinstance_set.all.count():
            raise ValidationError(
                ('This quantity of' + str(product.model) + 'is not available at the moment'))

        # Remember to always return the cleaned data.
        return data


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'body')
        widgets = {
            'name': TextInput(attrs={'aria-required': "true",
                                     'name': "contact-form-name",
                                     'class': "form-control",
                                     'placeholder': "Enter your name",
                                     'aria-invalid': "true"
                                     }),

            'body': Textarea(attrs={'name': "contact-form-message",
                                    'rows': "1",
                                    'class': "text-area-messge form-control",
                                    'placeholder': "Aa",
                                    'aria-required': "true",
                                    'aria-invalid': "false"
                                    }),
        }
