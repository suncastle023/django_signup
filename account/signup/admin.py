from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser

class CustomUserAdmin(UserAdmin):

    list_display = ('id', 'name', 'email', 'major', 'nickname', 'phone_number','age', 'hobbies', 'photo')
    search_fields = ('id', 'name', 'email', 'nickname')
    fieldsets = (
        (None, {'fields': ('id', 'password')}),
        (_('Personal info'), {'fields': ('name', 'email', 'major', 'nickname', 'phone_number')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {'classes': ('wide',), 'fields': ('id', 'name', 'email', 'password', 'major', 'nickname', 'phone_number')}),
    )
    ordering = ('id',)
    list_filter = ('major',)
    filter_horizontal = ()

admin.site.register(CustomUser, CustomUserAdmin)
