from django import forms
from .models import Property, PropertyImage

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = [
            'title', 'description', 'property_type', 'category', 'price',
            'bedrooms', 'bathrooms', 'area', 'address', 'city', 'state', 
            'pincode', 'parking', 'furnished', 'balcony', 'gym', 'swimming_pool'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'property_type': forms.Select(attrs={'class': 'form-select'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'bedrooms': forms.NumberInput(attrs={'class': 'form-control'}),
            'bathrooms': forms.NumberInput(attrs={'class': 'form-control'}),
            'area': forms.NumberInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'pincode': forms.TextInput(attrs={'class': 'form-control'}),
            'parking': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'furnished': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'balcony': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'gym': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'swimming_pool': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class PropertyImageForm(forms.ModelForm):
    class Meta:
        model = PropertyImage
        fields = ['image', 'caption']
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'caption': forms.TextInput(attrs={'class': 'form-control'}),
        }

class PropertySearchForm(forms.Form):
    PROPERTY_TYPES = (
        ('', 'All Types'),
        ('rent', 'For Rent'),
        ('sell', 'For Sale'),
    )
    
    PROPERTY_CATEGORIES = (
        ('', 'All Categories'),
        ('apartment', 'Apartment'),
        ('house', 'House'),
        ('villa', 'Villa'),
        ('studio', 'Studio'),
        ('room', 'Room'),
        ('commercial', 'Commercial'),
    )
    
    search = forms.CharField(
        max_length=200, 
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Search by title, city, or description'})
    )
    property_type = forms.ChoiceField(
        choices=PROPERTY_TYPES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    category = forms.ChoiceField(
        choices=PROPERTY_CATEGORIES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    city = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'})
    )
    min_price = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Min Price'})
    )
    max_price = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Max Price'})
    )
    bedrooms = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Min Bedrooms'})
    )
