from django.contrib import admin
from .models import Enquiry, Complaint, Feedback

class EnquiryAdmin(admin.ModelAdmin):
    list_display = ('user', 'property', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('user__username', 'property__title', 'message')
    readonly_fields = ('created_at',)

class ComplaintAdmin(admin.ModelAdmin):
    list_display = ('user', 'property', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'property__title', 'subject', 'description')
    readonly_fields = ('created_at',)

class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'property', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('user__username', 'property__title', 'comment')
    readonly_fields = ('created_at',)

admin.site.register(Enquiry, EnquiryAdmin)
admin.site.register(Complaint, ComplaintAdmin)
admin.site.register(Feedback, FeedbackAdmin)
