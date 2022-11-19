import os
# os.add_dll_directory(r"C:\Program Files (x86)\GTK2-Runtime\bin")
# from weasyprint import HTML
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.views import generic
from django.views.generic import View
from django.contrib.auth import authenticate, login
from .forms import AddToCart, UserRegisterForm  # , CommentForm
from .models import Category, Vendor, Product, ProductInstance, PersonalDetails  # , Comment
from django.contrib import messages
from django.template import RequestContext
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.db.models import Count
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.template.loader import render_to_string


# Create your views here.


def percent_save(price, discount_price):
    return 100*(price - discount_price)/price


def index(request):
    paginate_by = 10
    """Home page view function"""
    products = Product.objects.all()
    available_products = ProductInstance.objects.filter(status__exact='a')
    num_available_products = available_products.count()
    categories = Category.objects.all()
    vendors = Vendor.objects.all()
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    productinstance_list = ProductInstance.objects.filter(
        status__exact='r', buyer_id=request.user.id).order_by('purchase_date')

    amount_in_cart = productinstance_list.count()
    total_price = 0
    for i in range(len(productinstance_list)):
        total_price += productinstance_list[i].product.discount_price

    context = {
        'products': products,
        'available_products': available_products,
        'num_available_products': num_available_products,
        'categories': categories,
        'vendors': vendors,
        'num_visits': num_visits,
        'amount_in_cart': amount_in_cart,
        'total_price': total_price,
    }
    # Render the HTML template inde.html with the data in the context
    # variable
    return render(request, 'base_generic.html', context=context)


def pdf_html(request):
    addtocart_form = AddToCart()
    products = Product.objects.all()
    productinstance_list = ProductInstance.objects.filter(
        status__exact='r', buyer=request.user).order_by('purchase_date')

    billing_info = PersonalDetails.objects.filter(
        buyer=request.user)

    amount_in_cart = productinstance_list.count()
    total_price = 0
    for i in range(len(productinstance_list)):
        total_price += productinstance_list[i].product.discount_price

    context = {
        'products': products,
        'amount_in_cart': amount_in_cart,
        'total_price': total_price,
        'vendors': Vendor.objects.all(),
        'categories': Category.objects.all(),
        'productinstance_list': productinstance_list,
        'billing_info': billing_info,
    }
    return render(request, 'showcase/pdf_template.html', context=context)


class ProductListView(generic.ListView):
    """The generic view will query the database to get all 
    records for the specified model (Book) then render a template 
    located at /showcase/templates/showcase/product_list.html"""
    model = Product
    context_object_name = 'products'
    template_name = 'showcase/product_list.html'
    paginate_by = 9

    def get_context_data(self, **kwargs):
        """override get_context_data() in order to pass additional
        context variables to the template """

        productinstance_list = ProductInstance.objects.filter(
            status__exact='r', buyer=self.request.user.id).order_by('purchase_date')

        amount_in_cart = productinstance_list.count()
        total_price = 0
        for i in range(len(productinstance_list)):
            total_price += productinstance_list[i].product.discount_price

        # Call the base implementation first to get the context
        context = super(ProductListView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['categories'] = Category.objects.all()
        context['amount_in_cart'] = amount_in_cart
        context['total_price'] = total_price
        return context


class ProductDetailView(generic.DetailView, generic.edit.ProcessFormView):
    model = Product
    template_name = 'showcase/product_detail.html'
    context_object = {"addtocart_form": AddToCart}

    def post(self, request, *args, **kwargs):
        product = get_object_or_404(Product, pk=self.kwargs.get('pk'))
        addtocart_form = AddToCart(data=request.POST, instance=product)
        productinstance = ProductInstance.objects.filter(
            status__exact='a', product=product)
        # Check if the form is valid:

        if addtocart_form.is_valid():
            data = addtocart_form.cleaned_data['quantity_in_cart']

            # check if amount added to cart is not greater than available quantity.
            if data > ProductInstance.objects.filter(product=product, status__exact='a').count():
                raise ValidationError(
                    ('This quantity of' + str(product.model) + 'is not available at the moment'))
            amt = addtocart_form.cleaned_data['quantity_in_cart']
            product_instance_update = list(productinstance[:amt])
            addtocart_form.save()

            for i in range(amt):

                product_instance_update[i].status = 'r'
                product_instance_update[i].buyer = request.user
                print(product_instance_update[i])
                product_instance_update[i].save()

            ProductInstance.objects.bulk_update(
                product_instance_update, ['status', 'buyer'])

            # addtocart_form.save()
            messages.success(
                request, 'Item added to cart successfully.')
            # redirect to a new URL:
            # return HttpResponseRedirect(reverse('showcase:cart_products'))
            return redirect('showcase:cart_products')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        addtocart_form = AddToCart()
        product = get_object_or_404(Product, pk=self.kwargs.get('pk'))

        num_instances_available = ProductInstance.objects.filter(product=product,
            status__exact='a').count()

        productinstance_list = ProductInstance.objects.filter(
            status__exact='r', buyer=self.request.user.id).order_by('purchase_date')

        amount_in_cart = productinstance_list.count()
        total_price = 0
        for i in range(len(productinstance_list)):
            total_price += productinstance_list[i].product.discount_price

        context['num_instances_available'] = num_instances_available
        context['categories'] = Category.objects.all()
        context['vendors'] = Vendor.objects.all()
        context['product'] = product
        context['amount_in_cart'] = amount_in_cart
        context['total_price'] = total_price
        context['addtocart_form'] = addtocart_form

        return context


class CategoryProductsListView(generic.ListView):
    model = Product
    paginate_by = 12
    context_object_name = 'products'
    template_name = 'showcase/category_products.html'

    def get_queryset(self):
        category = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return Product.objects.filter(category=category)

    def get_context_data(self, **kwargs):
        context = super(CategoryProductsListView,
                        self).get_context_data(**kwargs)
        category = get_object_or_404(Category, pk=self.kwargs.get('pk'))

        productinstance_list = ProductInstance.objects.filter(
            status__exact='r', buyer=self.request.user.id).order_by('purchase_date')

        amount_in_cart = productinstance_list.count()
        total_price = 0
        for i in range(len(productinstance_list)):
            total_price += productinstance_list[i].product.discount_price

        context['categories'] = Category.objects.all()
        context['vendors'] = Vendor.objects.all()
        context['amount_in_cart'] = amount_in_cart
        context['total_price'] = total_price
        context['category'] = category
        return context


class VendorProductsListView(generic.ListView):
    model = Product
    paginate_by = 9
    context_object_name = 'products'
    template_name = 'showcase/vendor_products.html'

    def get_queryset(self):
        vendor = get_object_or_404(Vendor, pk=self.kwargs.get('pk'))
        return Product.objects.filter(vendor=vendor)

    def get_context_data(self, **kwargs):
        context = super(VendorProductsListView,
                        self).get_context_data(**kwargs)
        vendor = get_object_or_404(Vendor, pk=self.kwargs.get('pk'))

        productinstance_list = ProductInstance.objects.filter(
            status__exact='r', buyer=self.request.user.id).order_by('purchase_date')

        amount_in_cart = productinstance_list.count()
        total_price = 0
        for i in range(len(productinstance_list)):
            total_price += productinstance_list[i].product.discount_price

        context['vendors'] = Vendor.objects.all()
        context['categories'] = Category.objects.all()
        context['vendor'] = vendor
        context['amount_in_cart'] = amount_in_cart
        context['total_price'] = total_price
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


class SoldProductsByUserListview(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing products sold to current user."""
    model = ProductInstance
    template_name = 'showcase/productinstance_list_sold_buyer.html'
    paginate_by = 10

    def get_queryset(self):
        return ProductInstance.objects.filter(buyer=self.request.user.id).filter(status__exact='r').order_by('purchase_date')


class ProductUpdate(UpdateView):
    model = Product
    fields = ['quantity_in_cart']
    template_name = 'showcase/product_form.html'

    def form_valid(self, form):

        productinstance = ProductInstance.objects.filter(
            status__exact='r')
        products_quantity = []
        for instance in productinstance:
            products_quantity.append(instance.product.quantity_in_cart)

        for i in range(len(products_quantity)):
            if i < (len(products_quantity)-1):
                if products_quantity[i] == products_quantity[i + 1]:
                    products_quantity.remove(products_quantity[i + 1])

        for quantity in products_quantity:
            for j in range(quantity):
                productinstance[j].status = 'a'
                break

                productinstance[j].buyer = self.request.user
                productinstance[j].save()

        ProductInstance.objects.bulk_update(
            productinstance, ['status', 'buyer'])

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('showcase:cart_products')


class Cart(generic.ListView):
    model = ProductInstance
    template_name = 'showcase/cart.html'

    def get(self, request, *args, **kwargs):
        self.context = super().get(request, **kwargs)
        # productinstance = get_object_or_404(Product, pk=self.kwargs.get('pk'))
        addtocart_form = AddToCart()
        products = Product.objects.all()
        productinstance_list = ProductInstance.objects.filter(
            status__exact='r', buyer_id=request.user.id).order_by('purchase_date')

        billing_info = PersonalDetails.objects.filter(
            buyer=request.user)


        amount_in_cart = productinstance_list.count()
        total_price = 0
        for i in range(len(productinstance_list)):
            total_price += productinstance_list[i].product.discount_price

        self.context = {
            'products': products,
            'amount_in_cart': amount_in_cart,
            'total_price': total_price,
            'vendors': Vendor.objects.all(),
            'categories': Category.objects.all(),
            'productinstance_list': productinstance_list,
            'billing_info': billing_info,
        }
        return render(request, self.template_name, self.context)

    # def html_to_pdf_view(request):
    #     html_string = render_to_string('showcase/pdf_template.html')

    #     html = HTML(string=html_string)
    #     html.write_pdf(target='/tmp/mypdf.pdf')

    #     fs = FileSystemStorage('/tmp')
    #     with fs.open('mypdf.pdf') as pdf:
    #         response = HttpResponse(pdf, content_type='application/pdf')
    #         response['Content-Disposition'] = 'attachment; filename="mypdf.pdf"'
    #         return response

    #     return response


class PersonalDetailsUpdate(UpdateView):
    model = PersonalDetails
    fields = ['first_name', 'last_name', 'phone_number',
              'address_line_1', 'address_line_2', 'country', 'state', 'city', 'zip_code']
    template_name = 'showcase/billing_info.html'
    context = {}
    # context_object_name = 'personaldetails'

    def get_context_data(self, *args, **kwargs):
        self.context = super(PersonalDetailsUpdate,
                             self).get_context_data(**kwargs)
        productinstance_list = ProductInstance.objects.filter(
            status__exact='r', buyer=self.request.user.id).order_by('purchase_date')

        amount_in_cart = productinstance_list.count()
        total_price = 0
        for i in range(len(productinstance_list)):
            total_price += productinstance_list[i].product.discount_price

        self.context['vendors'] = Vendor.objects.all()
        self.context['categories'] = Category.objects.all()
        self.context['amount_in_cart'] = amount_in_cart
        self.context['total_price'] = total_price

        return self.context

    def get_success_url(self):
        return reverse('showcase:cart_products')


class EnrolCustomerCreate(CreateView):
    model = PersonalDetails
    fields = ['first_name', 'last_name', 'phone_number',
              'address_line_1', 'address_line_2', 'country', 'state', 'city', 'zip_code']
    template_name = 'registration/enrol_customer_form.html'
    context = {}
    context_object_name = 'personaldetails'

    def get_context_data(self, *args, **kwargs):
        self.context = super(EnrolCustomerCreate,
                             self).get_context_data(**kwargs)
        productinstance_list = ProductInstance.objects.filter(
            status__exact='r', buyer=self.request.user.id).order_by('purchase_date')

        amount_in_cart = productinstance_list.count()
        total_price = 0
        for i in range(len(productinstance_list)):
            total_price += productinstance_list[i].product.discount_price

        success_message = "Successful"

        self.context['success_message'] = success_message

        self.context['vendors'] = Vendor.objects.all()
        self.context['categories'] = Category.objects.all()
        self.context['amount_in_cart'] = amount_in_cart
        self.context['total_price'] = total_price

        return self.context

    def form_valid(self, form):
        form.instance.buyer = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('login')


class UserRegisterView(View):
    """
      View to let users register
    """
    template_name = 'registration/register.html'
    context = {
        "register_form": UserRegisterForm()
    }

    def get(self, request):
        success_message = "Successful"

        self.context['success_message'] = success_message

        self.context['vendors'] = Vendor.objects.all()
        self.context['categories'] = Category.objects.all()
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):

        register_form = UserRegisterForm(request.POST)

        if register_form.is_valid():
            user = register_form.save(commit=False)
            user.is_active = True
            user.is_staff = True
            user.save()
            login(request, user)
            messages.success(
                request, f'Hi {user.username}, your registration was successful!! .')

            return redirect('showcase:enrol-customer-create')

        else:
            messages.error(request, "Please provide valid information.")
            # Redirect user to register page
            return render(request, self.template_name, self.context_object)

    def get_success_url(self):
        return reverse('showcase:enrol-customer-create')
