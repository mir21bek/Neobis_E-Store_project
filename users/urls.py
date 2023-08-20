from django.urls import path
from .views import UserRegisterView, ConfirmEmailView, ProfileCreateView, ProfileRetrieveUpdateView
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('api/refresh/', TokenRefreshView.as_view()),
    path('confirm-email/<str:token>/', ConfirmEmailView.as_view(), name='confirm-email'),
    path('profile-create/', ProfileCreateView.as_view(), name='profile-create'),
    path('profile-update/', ProfileRetrieveUpdateView.as_view(), name='profile-update'),
]
