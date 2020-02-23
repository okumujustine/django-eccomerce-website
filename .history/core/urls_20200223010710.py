from django.urls import path,include

app_name = 'core'

from .views import  (
    HomeView,
    CheckoutView,
    products,
    ItemDetailView,
    add_to_cart,
    OrderSummaryView,
    remove_from_cart,timezone,
    remove_single_item_from_cart
    )
urlpatterns = [
    path('', HomeView.as_view(), name='item_list'),
    path('products/', products, name='products'),
    path('product/<slug>/', ItemDetailView.as_view(), name='product'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    
    path('add_to_cart/<slug>/', add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<slug>/', remove_from_cart, name='remove_from_cart'),
    path('remove_item_from_cart/<slug>/', remove_single_item_from_cart, name='remove_single_item_from_cart'),

    path('order-summary/', OrderSummaryView.as_view(), name='order-summary')
]