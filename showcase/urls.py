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
    path(
        route='category/<int:pk>',
        view=views.CategoryDetailView.as_view(),
        name='category_detail'
    ),
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
]
