from django.urls import path
from .views import CategoryListView, ProductListView, ProductDetailView, ProductCreateUpdateApiView, SaleProductApiView

urlpatterns = [
    path('category/', CategoryListView.as_view(), name='category'),
    path('products/', ProductListView.as_view(), name='products'),
    path('products/<int:pk>/', ProductDetailView.as_view()),
    path('product-create/', ProductCreateUpdateApiView.as_view(), name='product-create'),
    path('sale-product/', SaleProductApiView.as_view(), name='sale-product'),
]
