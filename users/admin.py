from django.contrib import admin
from .models import UserModel, Profile


@admin.register(UserModel)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username')


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('profile_user', 'first_name', 'last_name', 'city', 'phone_number')
