from django.urls import path
from .views import (CategoryListView, ProductListView,
                    ProductDetailView, ProductCreateUpdateApiView,
                    SaleProductApiView, RatingView, CommentView)

urlpatterns = [
    path('category/', CategoryListView.as_view(), name='category'),
    path('', ProductListView.as_view(), name='products'),
    path('products/<int:pk>/', ProductDetailView.as_view()),
    path('product-create/', ProductCreateUpdateApiView.as_view(), name='product-create'),
    path('sale-product/', SaleProductApiView.as_view(), name='sale-product'),
    path('rating/', RatingView.as_view(), name='rating'),
    path('comment/', CommentView.as_view(), name='comment'),
]
