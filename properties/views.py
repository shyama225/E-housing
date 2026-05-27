from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse
from .models import Property, PropertyImage
from .forms import PropertyForm, PropertyImageForm, PropertySearchForm
from communications.models import Enquiry

def property_list(request):
    form = PropertySearchForm(request.GET or None)
    properties = Property.objects.filter(is_approved=True, is_available=True)
    
    if form.is_valid():
        search = form.cleaned_data.get('search')
        property_type = form.cleaned_data.get('property_type')
        category = form.cleaned_data.get('category')
        city = form.cleaned_data.get('city')
        min_price = form.cleaned_data.get('min_price')
        max_price = form.cleaned_data.get('max_price')
        bedrooms = form.cleaned_data.get('bedrooms')
        
        if search:
            properties = properties.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(city__icontains=search)
            )
        
        if property_type:
            properties = properties.filter(property_type=property_type)
        
        if category:
            properties = properties.filter(category=category)
        
        if city:
            properties = properties.filter(city__icontains=city)
        
        if min_price:
            properties = properties.filter(price__gte=min_price)
        
        if max_price:
            properties = properties.filter(price__lte=max_price)
        
        if bedrooms:
            properties = properties.filter(bedrooms__gte=bedrooms)
    
    paginator = Paginator(properties, 12)
    page_number = request.GET.get('page')
    properties = paginator.get_page(page_number)
    
    context = {
        'properties': properties,
        'form': form,
    }
    return render(request, 'properties/property_list.html', context)

def property_detail(request, pk):
    property_obj = get_object_or_404(Property, pk=pk, is_approved=True)
    images = property_obj.images.all()
    
    # Get related properties (same city, different property)
    related_properties = Property.objects.filter(
        city=property_obj.city,
        is_approved=True,
        is_available=True
    ).exclude(pk=property_obj.pk)[:4]
    
    context = {
        'property': property_obj,
        'images': images,
        'related_properties': related_properties,
    }
    return render(request, 'properties/property_detail.html', context)

@login_required
def add_property(request):
    if request.user.user_type != 'owner':
        messages.error(request, 'Only property owners can add properties.')
        return redirect('properties:list')
    
    if request.method == 'POST':
        form = PropertyForm(request.POST)
        if form.is_valid():
            property_obj = form.save(commit=False)
            property_obj.owner = request.user
            property_obj.save()
            messages.success(request, 'Property added successfully! It will be visible after admin approval.')
            return redirect('properties:my_properties')
    else:
        form = PropertyForm()
    
    return render(request, 'properties/add_property.html', {'form': form})

@login_required
def edit_property(request, pk):
    property_obj = get_object_or_404(Property, pk=pk, owner=request.user)
    
    if request.method == 'POST':
        form = PropertyForm(request.POST, instance=property_obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Property updated successfully!')
            return redirect('properties:my_properties')
    else:
        form = PropertyForm(instance=property_obj)
    
    return render(request, 'properties/edit_property.html', {
        'form': form,
        'property': property_obj
    })

@login_required
def delete_property(request, pk):
    property_obj = get_object_or_404(Property, pk=pk, owner=request.user)
    
    if request.method == 'POST':
        property_obj.delete()
        messages.success(request, 'Property deleted successfully!')
        return redirect('properties:my_properties')
    
    return render(request, 'properties/delete_property.html', {'property': property_obj})

@login_required
def my_properties(request):
    if request.user.user_type != 'owner':
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    properties = Property.objects.filter(owner=request.user).order_by('-created_at')
    
    paginator = Paginator(properties, 10)
    page_number = request.GET.get('page')
    properties = paginator.get_page(page_number)
    
    return render(request, 'properties/my_properties.html', {'properties': properties})

@login_required
def manage_property_images(request, pk):
    property_obj = get_object_or_404(Property, pk=pk, owner=request.user)
    images = property_obj.images.all()
    
    if request.method == 'POST':
        form = PropertyImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.property = property_obj
            image.save()
            messages.success(request, 'Image added successfully!')
            return redirect('properties:manage_images', pk=pk)
    else:
        form = PropertyImageForm()
    
    context = {
        'property': property_obj,
        'images': images,
        'form': form,
    }
    return render(request, 'properties/manage_images.html', context)

@login_required
def delete_property_image(request, pk, image_id):
    property_obj = get_object_or_404(Property, pk=pk, owner=request.user)
    image = get_object_or_404(PropertyImage, pk=image_id, property=property_obj)
    
    if request.method == 'POST':
        image.delete()
        messages.success(request, 'Image deleted successfully!')
    
    return redirect('properties:manage_images', pk=pk)

def is_admin(user):
    return user.user_type == 'admin'

@login_required
@user_passes_test(is_admin)
def manage_properties(request):
    properties = Property.objects.all().order_by('-created_at')
    
    paginator = Paginator(properties, 15)
    page_number = request.GET.get('page')
    properties = paginator.get_page(page_number)
    
    return render(request, 'properties/manage_properties.html', {'properties': properties})

@login_required
@user_passes_test(is_admin)
def approve_property(request, pk):
    property_obj = get_object_or_404(Property, pk=pk)
    property_obj.is_approved = True
    property_obj.save()
    messages.success(request, f'Property "{property_obj.title}" has been approved.')
    return redirect('properties:manage_properties')

@login_required
@user_passes_test(is_admin)
def reject_property(request, pk):
    property_obj = get_object_or_404(Property, pk=pk)
    property_obj.is_approved = False
    property_obj.save()
    messages.success(request, f'Property "{property_obj.title}" has been rejected.')
    return redirect('properties:manage_properties')

@login_required
def toggle_availability(request, pk):
    property_obj = get_object_or_404(Property, pk=pk, owner=request.user)
    property_obj.is_available = not property_obj.is_available
    property_obj.save()
    
    status = 'available' if property_obj.is_available else 'unavailable'
    messages.success(request, f'Property marked as {status}.')
    
    return redirect('properties:my_properties')
