from django import forms
from django.contrib import admin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AdminPasswordChangeForm
from django.contrib.auth.admin import UserAdmin
from .models import MyUser


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = MyUser
        fields = '__all__'


class MyUserChangeForm(UserChangeForm):
    class Meta:
        model = MyUser
        fields = '__all__'


class MyUserAdmin(UserAdmin):
    add_form = MyUserCreationForm
    form = MyUserChangeForm
    list_display = ('email', 'full_name', )
    list_filter = ('is_staff', )
    readonly_fields = ('is_superuser', 'last_login', 'joined_date', )

    fieldsets = (
        (None, {
            'fields': (
                'email',
                'password',
                'last_name',
                'first_name',
                'is_superuser',
                'nickname',
                'img_profile',
            )
        }),
        ('Permissions', {
            'fields': (
                'groups',
                'user_permissions'
            )
        }),
        ('Important dates', {
            'fields': (
                'last_login',
                'joined_date'
            )
        }),
    )
    add_fieldsets = (
        (None, {
            'fields': (
                'email',
                'password1',
                'password2',
                'last_name',
                'first_name',
                'nickname',
                'img_profile',
                'is_staff',
            )
        }),
    )
    ordering = ('email', )


admin.site.register(MyUser, MyUserAdmin)