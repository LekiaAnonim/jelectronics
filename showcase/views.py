from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.views import generic
from .forms import AddToCart
from .models import Category, Vendor, Product, ProductInstance
# Create your views here.

def percent_save(price, discount_price):
    return 100*(price - discount_price)/price

def index(request):
    """Home page view function"""
    # Available Products (status = 'a')
    products = Product.objects.all()
    available_products = ProductInstance.objects.filter(status__exact='a')
    num_available_products = available_products.count()
    categories = Category.objects.all()
    vendors = Vendor.objects.all()
    # product = Product.objects.get(pk=primary_key)
    # save = 100*(product.price - product.discount_price)/price
    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1


    context = {
        'products': products,
        'available_products': available_products,
        'num_available_products': num_available_products,
        'categories': categories,
        'vendors': vendors,
        'num_visits': num_visits,
    }
    # Render the HTML template inde.html with the data in the context
    # variable
    return render(request, 'base_generic.html', context=context)

class ProductListView(generic.ListView):
    """The generic view will query the database to get all 
    records for the specified model (Book) then render a template 
    located at /showcase/templates/showcase/product_list.html"""
    model = Product
    context_object_name = 'products'
    template_name = 'showcase/product_list.html'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        """override get_context_data() in order to pass additional
        context variables to the template """

        # Call the base implementation first to get the context
        context = super(ProductListView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['some_data'] = 'This is just some data'
        return context

class ProductDetailView(generic.DetailView):
    model = Product
    template_name = 'showcase/product_detail.html'

    @login_required
    def add_to_cart(self, request, pk):
        product_instance = get_object_or_404(ProductInstance, pk=pk)

        # If this is a POST request then process the Form data
        if request.method == 'POST':
            form = AddToCart(request.POST)
            productinstance = ProductInstance.objects.filter(status__exact='a')
            # Check if the form is valid:
            if form.is_valid():
                for i in range(form.cleaned_data['quantity']):
                    productinstance[i].status = 'r'
                    product_instance.save()

                    # redirect to a new URL:
                    return HttpResponseRedirect(reverse('bought_products'))
        context = {
            'form': form,
            'product_instance': product_instance,
        }

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        # Available books (status = 'a')
        num_instances_available = ProductInstance.objects.filter(status__exact='a').count()

        context['num_instances_available'] = num_instances_available
        context['categories'] = Category.objects.all()
        # context['form'] = form
        # context['product_instance'] = product_instance

        return context


class CategoryListView(generic.ListView):
    model = Category
    paginate_by = 4

class CategoryDetailView(generic.DetailView):
    model = Category


class VendorListView(generic.ListView):
    model = Vendor
    paginate_by = 4


class VendorDetailView(generic.DetailView):
    model = Vendor

from django.contrib.auth.mixins import LoginRequiredMixin
class SoldProductsByUserListview(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing products sold to current user."""
    model = ProductInstance
    template_name = 'showcase/productinstance_list_sold_buyer.html'
    paginate_by = 10

    def get_queryset(self):
        return ProductInstance.objects.filter(buyer=self.request.user).filter(status__exact='r').order_by('purchase_date')


# @login_required
# def add_to_cart(request, pk):
#     product_instance = get_object_or_404(ProductInstance, pk=pk)

#     # If this is a POST request then process the Form data
#     if request.method == 'POST':
#         form = AddToCart(request.POST)
#         productinstance = ProductInstance.objects.filter(status__exact='a')
#         # Check if the form is valid:
#         if form.is_valid():
#             for i in range(form.cleaned_data['quantity']):
#                 productinstance[i].status = 'r'
#                 product_instance.save()

#                 # redirect to a new URL:
#                 return HttpResponseRedirect(reverse('bought_products'))
#     context = {
#         'form': form,
#         'product_instance': product_instance,
#     }
#     return render(request, 'showcase/product_detail.html', context)
