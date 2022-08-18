from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.views import generic
from .forms import AddToCart, CommentForm
from .models import Category, Vendor, Product, ProductInstance, Comment
from django.contrib import messages
from django.template import RequestContext


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


class ProductDetailView(generic.DetailView, generic.edit.ProcessFormView):
    model = Product
    template_name = 'showcase/product_detail.html'

    def post(self, request, *args, **kwargs):
        product = get_object_or_404(Product, pk=self.kwargs.get('pk'))
        # comments = product.comments.filter(active=True)
        if request.method == 'POST':
            comment_form = CommentForm(data=self.request.POST)
            if comment_form.is_valid():
                parent_obj = None
                try:
                    parent_id = int(request.POST.get('parent_id'))
                    print(parent_id)
                except:
                    parent_id = None
                # if parent id has been submitted get parent_obj id
                if parent_id:
                    parent_obj = Comment.objects.get(id=parent_id)
                    # if parent object exist
                    if parent_obj:
                        reply_comment = comment_form.save(commit=False)
                        # assign parent_object to reply comment
                        reply_comment.parent = parent_obj

                # normal comment
                comment = comment_form.save(commit=False)
                comment.product = product
                # comment.name = request.User
                # comment.body = self.get_object()
                comment.save()
                # return HttpResponseRedirect(product.get_absolute_url())

            self.object = self.get_object()
            context = super(ProductDetailView,
                            self).get_context_data(**kwargs)
            context['comment_form'] = CommentForm
            return self.render_to_response(context=context)
        else:
            self.object = self.get_object()
            context = super(ProductDetailView, self).get_context_data(**kwargs)
            context['comment_form'] = comment_form
            return self.render_to_response(context=context)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        # Available books (status = 'a')
        # new_comment = None
        comment_form = CommentForm()
        product = get_object_or_404(Product, pk=self.kwargs.get('pk'))
        comments = product.comments.filter(active=True)
        num_instances_available = ProductInstance.objects.filter(
            status__exact='a').count()

        context['num_instances_available'] = num_instances_available
        context['categories'] = Category.objects.all()
        context['product'] = product
        context['comments'] = comments
        # context['new_comment'] = new_comment
        context['comment_form'] = comment_form

        return context


# class CommentCreateView(generic.CreateView):
#     model = Comment
#     form_class = CommentForm
#     # new_comment = None

#     def form_valid(self, form):
#         # comment_form = CommentForm(data=self.request.POST)
#         # new_comment = comment_form.save(commit=False)
#         comment = form.save(commit=False)
#         comment.product = get_object_or_404(Product,
#                                             model=self.kwargs.get('model'))
#         comment.save()
#         messages.success(self.request, "Comment Added successfully")
#         return redirect('showcase:product_detail', comment.product.model)


# @method_decorator(csrf_exempt, name='dispatch')
# @method_decorator(ensure_csrf_cookie, name='dispatch')
# class ProductCommentList(generic.ListView):
#     model = Comment
#     context_object_name = "comments"
#     paginate_by = 10
#     template_name = "showcase/product_detail.html"

#     def get_queryset(self):
#         product = get_object_or_404(Product, model=self.kwargs.get('model'))
#         queryset = Comment.objects.filter(product=product)
#         return queryset

#     def get_context_data(self, **kwargs):
#         context = super(ProductCommentList, self).get_context_data(**kwargs)
#         product = get_object_or_404(Product,
#                                     product=self.kwargs.get('product'))
#         context['product'] = product
#         context['comment_form'] = CommentForm()
#         context['comments'] = product.comments.filter(active=True)
#         return context


class CategoryArticlesListView(generic.ListView):
    model = Product
    paginate_by = 12
    context_object_name = 'products'
    template_name = 'showcase/category_products.html'


    def get_queryset(self):
        category = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return Product.objects.filter(category=category)

    def get_context_data(self, **kwargs):
        context = super(CategoryArticlesListView, self).get_context_data(**kwargs)
        category = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        context['category'] = category
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
        return ProductInstance.objects.filter(buyer=self.request.user).filter(status__exact='r').order_by('purchase_date')


class Cart(generic.ListView):
    model = ProductInstance
    template_name = 'showcase/cart.html'
    global productinstance_list
    productinstance_list = ProductInstance.objects.filter().filter(
        status__exact='a').order_by('purchase_date')
    # for inst in productinstance_list:
    #     print(inst.product.model)
    # def get_queryset(self):
    #     return ProductInstance.objects.filter(buyer=self.request.user).filter(status__exact='a').order_by('purchase_date')

    @login_required
    def add_to_cart(self, request, pk):
        product_instance = get_object_or_404(ProductInstance, pk=pk)
        productinstance_list = ProductInstance.objects.filter(
            buyer=self.request.user).filter(status__exact='a').order_by('purchase_date')
        # products = Product.objects.all()

        for inst in productinstance_list:
            print(inst)
        # If this is a POST request then process the Form data
        if request.method == 'POST':
            form = AddToCart(request.POST)
            productinstance = ProductInstance.objects.filter(status__exact='a')
            # Check if the form is valid:
            if form.is_valid():
                for i in range(form.cleaned_data['quantity']):
                    productinstance[i].status = 'r'
                    print(i)
                    product_instance.save()
                    messages.success(
                        request, 'Item added to cart successfully.')
                    # redirect to a new URL:
                    return HttpResponseRedirect(reverse('cart_products'))

        else:
            form = AddToCart()

        context = {
            'form': form,
            'product_instance': product_instance,
            # 'productinstance_list': productinstance_list,
        }
        return(request, showcase/cart.html, context)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        products = Product.objects.all()

        productinstance_list = ProductInstance.objects.filter(
        ).filter(status__exact='a').order_by('purchase_date')

        context = {
            'products': products,
            # 'product_instance': product_instance,
            'productinstance_list': productinstance_list,
        }
        return context
