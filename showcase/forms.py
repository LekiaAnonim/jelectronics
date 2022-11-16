from django import forms
from .models import Category, Vendor, Product, ProductInstance  # , Comment
from . import views

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.forms import ModelForm, TextInput, EmailInput, Textarea
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class AddToCart(forms.ModelForm):
    # quantity = forms.IntegerField(initial="1")

    class Meta:
        model = Product
        fields = ('quantity_in_cart',)


class UserRegisterForm(UserCreationForm):
    """
        Creates User registration form for signing up.
    """

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.pop("autofocus", None)

    email = forms.EmailField(max_length=254, required=True, widget=forms.EmailInput(attrs={
        "name": "email", "class": "input100",
        "placeholder": "Email"
    }
    ),
        help_text='Required. Input a valid email address.'
    )
    password1 = forms.CharField(label= "Password", widget=forms.PasswordInput(attrs={
        "name": "password", "class": "input100",
        "placeholder": "Password"
    }
    ),
    )

    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs={
        "name": "Confirm Password", "class": "input100",
        "placeholder": "Confirm Password"
    }

    ),
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {

            "username": forms.TextInput(attrs={
                "name": "username", "class": "input100",
                "placeholder": "Username"
            }),


        }

    def save(self, commit=True):
        user = super(UserRegisterForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
