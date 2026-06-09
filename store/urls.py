from django.urls import path
from .views import ProductListCreateView, CategoryListCreateView, ProductDetailView, CartDetailView, CartItemView, \
    OrderListView, OrderDetailView, CartOrderView

urlpatterns = [
    path('products/', ProductListCreateView.as_view()),
    path('categories/', CategoryListCreateView.as_view()),
    path('products/<int:pk>/', ProductDetailView.as_view()),
    path('cart/', CartDetailView.as_view()),
    path('cart/item/<int:pk>/', CartItemView.as_view()),
    path('orders/create/', CartOrderView.as_view()),
    path('orders/', OrderListView.as_view()),
    path('orders/<int:pk>/', OrderDetailView.as_view()),
]