from django.db import models
from django.contrib.auth import get_user_model
from properties.models import Property

User = get_user_model()

class Enquiry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enquiries')
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='enquiries')
    message = models.TextField()
    phone = models.CharField(max_length=15, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Enquiries'
    
    def __str__(self):
        return f"Enquiry from {self.user.username} for {self.property.title}"

class EnquiryResponse(models.Model):
    enquiry = models.ForeignKey(Enquiry, on_delete=models.CASCADE, related_name='responses')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"Response from {self.sender.username}"

class Complaint(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='complaints')
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='complaints')
    subject = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    owner_response = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Complaint by {self.user.username} - {self.subject}"

class Feedback(models.Model):
    RATING_CHOICES = (
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feedbacks')
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='feedbacks')
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ['user', 'property']  # One feedback per user per property
    
    def __str__(self):
        return f"Feedback by {self.user.username} - {self.rating} stars"
