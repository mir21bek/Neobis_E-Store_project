from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.utils.crypto import get_random_string

from decouple import config

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'password2']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({
                'password': 'Password did not match'
            })
        return attrs

    def create(self, validated_data):
        email = validated_data['email']
        user = User.objects.create(email=email, username = validated_data['username'])
        user.set_password(validated_data['password'])
        user.is_active = False
        user.activation_token = get_random_string(64)
        user.save()

        # Send a message on the email address
        current_site = get_current_site(self.context['request'])
        domain = current_site.domain
        protocol = 'https' if self.context['request'].is_secure() else 'http'
        confirmation_link = reverse('confirm-email', kwargs={'token': user.activation_token})

        subject = 'Подтверждение регистрации'
        message = f'Подтвердите вашу регистрацию по ссылке: \n\n{protocol}://{domain}{confirmation_link}'
        from_email = config('EMAIL_HOST_USER')
        to_email = email
        send_mail(subject, message, from_email, [to_email], fail_silently=False)
        return user
