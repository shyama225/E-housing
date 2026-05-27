from django.contrib import admin
from .models import Property, PropertyImage

class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1

class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'property_type', 'price', 'city', 'is_approved', 'created_at')
    list_filter = ('property_type', 'is_approved', 'city', 'created_at')
    search_fields = ('title', 'description', 'address', 'city')
    inlines = [PropertyImageInline]
    actions = ['approve_properties', 'reject_properties']
    
    def approve_properties(self, request, queryset):
        queryset.update(is_approved=True)
        self.message_user(request, f'{queryset.count()} properties were approved.')
    approve_properties.short_description = 'Approve selected properties'
    
    def reject_properties(self, request, queryset):
        queryset.update(is_approved=False)
        self.message_user(request, f'{queryset.count()} properties were rejected.')
    reject_properties.short_description = 'Reject selected properties'

admin.site.register(Property, PropertyAdmin)
admin.site.register(PropertyImage)
