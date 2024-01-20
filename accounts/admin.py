from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Organization

class UserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_agent', 'organization')
    fieldsets = (
        (None, {'fields': ('username', 'password', 'is_agent')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Organization', {'fields': ('organization',)}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )

admin.site.register(User, UserAdmin)
admin.site.register(Organization)


