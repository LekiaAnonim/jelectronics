import uuid
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.text import slugify
from cities_light.models import Region, Country
from cities_light.models import City
from smart_selects.db_fields import ChainedForeignKey
from django.utils.translation import gettext_lazy as _
from parler.models import TranslatableModel, TranslatedFields
# Create your models here.


class PersonalDetails(TranslatableModel):
    buyer = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True)
    translations = TranslatedFields(
        
        first_name=models.CharField(_('first_name'), max_length=255, null=True),
        last_name=models.CharField(_('last_name'), max_length=255, null=True),
        phone_number=models.CharField(
            _('phone_number'), max_length=255, null=True),
        address_line_1=models.CharField(
            _('address_line_1'), max_length=255, null=True),
        address_line_2=models.CharField(
            _('address_line_2'), max_length=255, null=True, blank=True),

        country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True),
        state = ChainedForeignKey(Region, chained_field="country", chained_model_field="country"),
        city = models.CharField(_('city'), max_length=255, null=True, blank=True),
        zip_code = models.CharField(_('zip_code'), max_length=255, null=True),
    )
    

    # class Meta:
    #     ordering = ['city', 'state', 'first_name']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def get_absolute_url(self):
        return reverse('showcase:billing-info', kwargs={'pk': self.pk})


class Category(TranslatableModel):
    """Model for representing product category."""

    translations = TranslatedFields(
        
        name = models.CharField(_('name'),
        max_length=250, help_text='Enter a product category (e.g TV, Fans)')
    )


    image = models.ImageField(null=True, blank=True,
                              upload_to='media/category_pics')

    def __str__(self):
        """String for representing the Model object."""
        return self.name


class Vendor(TranslatableModel):
    """Model for representing product vendor."""

    translations = TranslatedFields(
        name = models.CharField(_('name'),
        max_length=250, help_text='Enter a product category (e.g LG, Samsung)')
    )
    

    def __str__(self):
        """String for representing the Model object."""
        return self.name


class Product(TranslatableModel):
    """Model for representing product"""

    translations = TranslatedFields(
        model=models.CharField(_('model'),
        max_length=250, help_text='Enter product model', unique=True),
        price=models.FloatField(_('price'), null=True),
        discount_price=models.FloatField(
          null=True, blank=True),
        description=models.TextField(_('description'), null=True, blank=True),
        
    )
    quantity_in_cart=models.IntegerField(
        null=True, blank=True, help_text='Leave this field blank')
    # slug = models.SlugField(max_length=100)
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True,
                               help_text='Select a vendor for this product')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,
                                 null=True, help_text='Select a category for this product')
    
    image = models.ImageField(null=True, blank=True,
                              upload_to='media/product_pics')
    image2 = models.ImageField(null=True, blank=True,
                               upload_to='media/product_pics')
    image3 = models.ImageField(null=True, blank=True,
                               upload_to='media/product_pics')
    

    def __str__(self):
        """String for representing the Model object."""
        return self.model

    def get_absolute_url(self):
        return reverse('product_detail', args=[str(self.model)])


class ProductInstance(TranslatableModel):
    """This model is for a specific product that can be sold from the shop"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text='Unique ID for this particular product in the shop')
    product = models.ForeignKey(Product, on_delete=models.RESTRICT, null=True)
    purchase_date = models.DateField(null=True, auto_now=True, blank=True)
    SALE_STATUS = (
        ('a', 'Available'),
        ('m', 'Maintenance'),
        ('s', 'Sold'),
        ('r', 'Reserved'),
    )
    status=models.CharField(_('status'), choices=SALE_STATUS, blank=True,
                                default='a', max_length=1, help_text='Product availability')
    buyer=models.OneToOneField(
            User, on_delete=models.SET_NULL, null=True, blank=True)
    

    class Meta:
        ordering = ['purchase_date']

    def __str__(self):
        return f'{self.id} ({self.product.model})'

        #
    def get_absolute_url(self):
        return reverse('product_detail', args=[str(self.product.model)])



