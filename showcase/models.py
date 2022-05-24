import uuid
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.


class Category(models.Model):
    """Model for representing product category."""
    name = models.CharField(
        max_length=250, help_text='Enter a product category (e.g TV, Fans)')

    image = models.ImageField(null=True, blank=True,
                              upload_to='media/category_pics')

    def __str__(self):
        """String for representing the Model object."""
        return self.name


class Vendor(models.Model):
    """Model for representing product vendor."""
    name = models.CharField(
        max_length=250, help_text='Enter a product category (e.g LG, Samsung)')

    def __str__(self):
        """String for representing the Model object."""
        return self.name


class Product(models.Model):
    """Model for representing product"""
    model = models.CharField(
        max_length=250, help_text='Enter product model', unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True,
                               help_text='Select a vendor for this product')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,
                                 null=True, help_text='Select a category for this product')
    price = models.FloatField(null=True)
    image = models.ImageField(null=True, blank=True,
                              upload_to='media/product_pics')
    discount_price = models.FloatField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        """String for representing the Model object."""
        return self.model

    def get_absolute_url(self):
        return reverse('product_detail', args=[str(self.model)])


class ProductInstance(models.Model):
    """This model is for a specific product that can be sold from the shop"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text='Unique ID for this particular product in the shop')
    product = models.ForeignKey(Product, on_delete=models.RESTRICT, null=True)
    image = models.ImageField(null=True, blank=True,
                              upload_to='media/product_pics')
    purchase_date = models.DateField(null=True, auto_now=True, blank=True)
    buyer = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)
    SALE_STATUS = (
        ('a', 'Available'),
        ('m', 'Maintenance'),
        ('s', 'Sold'),
        ('r', 'Reserved'),
    )
    status = models.CharField(choices=SALE_STATUS, blank=True,
                              default='a', max_length=1, help_text='Product availability')

    class Meta:
        ordering = ['purchase_date']

    def __str__(self):
        return f'{self.id} ({self.product.model})'
        
        # 
    def get_absolute_url(self):
        return reverse('product_detail', args=[str(self.model)])

