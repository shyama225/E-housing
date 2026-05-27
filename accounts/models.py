from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse

class User(AbstractUser):
    USER_TYPES = (
        ('buyer', 'Buyer/Tenant'),
        ('owner', 'Property Owner'),
        ('admin', 'Administrator'),
    )
    
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default='buyer')
    is_approved = models.BooleanField(default=False)
    email = models.EmailField(unique=True)
    
    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"
    
    def get_dashboard_url(self):
        if self.user_type == 'admin':
            return reverse('admin_dashboard')
        elif self.user_type == 'owner':
            return reverse('owner_dashboard')
        else:
            return reverse('user_dashboard')

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=50, blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
