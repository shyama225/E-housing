from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()

class Property(models.Model):
    PROPERTY_TYPES = (
        ('rent', 'For Rent'),
        ('sell', 'For Sale'),
    )
    
    PROPERTY_CATEGORIES = (
        ('apartment', 'Apartment'),
        ('house', 'House'),
        ('villa', 'Villa'),
        ('studio', 'Studio'),
        ('room', 'Room'),
        ('commercial', 'Commercial'),
    )
    
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='properties')
    title = models.CharField(max_length=200)
    description = models.TextField()
    property_type = models.CharField(max_length=10, choices=PROPERTY_TYPES)
    category = models.CharField(max_length=20, choices=PROPERTY_CATEGORIES)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    bedrooms = models.PositiveIntegerField(default=1)
    bathrooms = models.PositiveIntegerField(default=1)
    area = models.PositiveIntegerField(help_text='Area in square feet')
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    is_approved = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Additional features
    parking = models.BooleanField(default=False)
    furnished = models.BooleanField(default=False)
    balcony = models.BooleanField(default=False)
    gym = models.BooleanField(default=False)
    swimming_pool = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Properties'
    
    def __str__(self):
        return f"{self.title} - {self.get_property_type_display()}"
    
    def get_absolute_url(self):
        return reverse('properties:detail', kwargs={'pk': self.pk})
    
    def get_main_image(self):
        main_image = self.images.first()
        return main_image.image.url if main_image else None

class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='properties/')
    caption = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"Image for {self.property.title}"
