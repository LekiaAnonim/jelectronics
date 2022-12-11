from django.urls import path

from . import views

app_name = 'showcase'

urlpatterns = [
    path(
        route='', 
        view=views.index,
        name='index'
    ),
    path(
        route='products/',
        view=views.ProductListView.as_view(), 
        name='products'
    ),
    path(
        route='product/<int:pk>',
        view=views.ProductDetailView.as_view(),
        name='product_detail'
    ),
    path(
        route='categories/',
        view=views.CategoryListView.as_view(),
        name='categories'
    ),
    # path(
    #     route='category/<int:pk>',
    #     view=views.CategoryDetailView.as_view(),
    #     name='category_detail'
    # ),
    path(
        route='vendors/',
        view=views.VendorListView.as_view(),
        name='vendors'
    ),
    path(
        route='vendor/<int:pk>',
        view=views.VendorDetailView.as_view(),
        name='vendor_detail'
    ),
    path(
        route='myproducts/',
        view=views.SoldProductsByUserListview.as_view(),
        name='bought_products'
    ),
    path(
        route='product/cart',
        view=views.Cart.as_view(),
        name='cart_products'
    ),
    path(
        route='category/<int:pk>',
        view=views.CategoryProductsListView.as_view(),
        name='category_products'
    ),
    path(
        route='vendor/<int:pk>/products',
        view=views.VendorProductsListView.as_view(),
        name='vendor_products'
    ),
    path('product/<int:pk>/remove/',
         views.ProductUpdate.as_view(), name='product-cart-update'),


    path('enrol-customer/create/', views.EnrolCustomerCreate.as_view(),
         name='enrol-customer-create'),

    path(
        route='account/register',
        view=views.UserRegisterView.as_view(),
        name='register'
    ),

    path(
        route='personaldetails/<int:pk>/billing-info',
        view=views.PersonalDetailsUpdate.as_view(),
        name='billing-info'
    ),
    path(
        route='order-summary/pdf_html',
        view=views.pdf_html,
        name='pdf_html'
    ),
]
