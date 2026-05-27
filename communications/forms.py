from django import forms
from .models import Enquiry, EnquiryResponse, Complaint, Feedback

class EnquiryForm(forms.ModelForm):
    class Meta:
        model = Enquiry
        fields = ['message', 'phone']
        widgets = {
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Write your enquiry message here...'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your phone number (optional)'
            }),
        }

class EnquiryResponseForm(forms.ModelForm):
    class Meta:
        model = EnquiryResponse
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Type your response here...'
            }),
        }

class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['subject', 'description']
        widgets = {
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Complaint subject'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe your complaint in detail...'
            }),
        }

class ComplaintResponseForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['status', 'owner_response']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
            'owner_response': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Your response to the complaint...'
            }),
        }

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(attrs={'class': 'form-select'}),
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Share your experience (optional)...'
            }),
        }
