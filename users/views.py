from django.shortcuts import redirect
from rest_framework.generics import CreateAPIView, GenericAPIView
from django.contrib.auth import get_user_model, login
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import RegisterSerializer

User = get_user_model()


class UserRegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = []


class ConfirmEmailView(GenericAPIView):
    def get(self, request, token):
        try:
            user = User.objects.get(activation_token=token)
            user.is_active = True
            user.save()

            login(request, user)
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'detail': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
