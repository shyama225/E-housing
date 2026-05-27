from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Profile

class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'user_type', 'is_approved', 'is_active', 'date_joined')
    list_filter = ('user_type', 'is_approved', 'is_active', 'date_joined')
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('user_type', 'is_approved')}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('user_type', 'is_approved')}),
    )

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'city', 'created_at')
    list_filter = ('city', 'created_at')
    search_fields = ('user__username', 'phone', 'city')

admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
