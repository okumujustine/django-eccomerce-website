from django.urls import path,include

app_name = 'core'

from .views import  (
    HomeView,
    checkout,
    products,
    ItemDetailView,
    add_to_cart,
    OrderSummaryView,
    remove_from_cart
    )
urlpatterns = [
    path('', HomeView.as_view(), name='item_list'),
    path('products/', products, name='products'),
    path('product/<slug>/', ItemDetailView.as_view(), name='product'),
    path('checkout/', checkout, name='checkout'),
    
    path('add_to_cart/<slug>/', add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<slug>/', remove_from_cart, name='remove_from_cart'),

    path('order-summary/' OrderSummaryView.as_view(), name='order-summary ')
]