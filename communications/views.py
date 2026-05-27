from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from properties.models import Property
from .models import Enquiry, EnquiryResponse, Complaint, Feedback
from .forms import EnquiryForm, EnquiryResponseForm, ComplaintForm, ComplaintResponseForm, FeedbackForm

@login_required
def send_enquiry(request, property_id):
    property_obj = get_object_or_404(Property, pk=property_id, is_approved=True)
    
    if request.method == 'POST':
        form = EnquiryForm(request.POST)
        if form.is_valid():
            enquiry = form.save(commit=False)
            enquiry.user = request.user
            enquiry.property = property_obj
            enquiry.save()
            messages.success(request, 'Your enquiry has been sent successfully!')
            return redirect('properties:detail', pk=property_id)
    else:
        form = EnquiryForm()
    
    context = {
        'form': form,
        'property': property_obj,
    }
    return render(request, 'communications/send_enquiry.html', context)

@login_required
def my_enquiries(request):
    if request.user.user_type not in ['buyer']:
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    enquiries = Enquiry.objects.filter(user=request.user).order_by('-created_at')
    
    paginator = Paginator(enquiries, 10)
    page_number = request.GET.get('page')
    enquiries = paginator.get_page(page_number)
    
    return render(request, 'communications/my_enquiries.html', {'enquiries': enquiries})

@login_required
def enquiry_detail(request, enquiry_id):
    enquiry = get_object_or_404(Enquiry, pk=enquiry_id)
    
    # Check if user has access to this enquiry
    if request.user != enquiry.user and request.user != enquiry.property.owner:
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    responses = enquiry.responses.all()
    
    if request.method == 'POST':
        form = EnquiryResponseForm(request.POST)
        if form.is_valid():
            response = form.save(commit=False)
            response.enquiry = enquiry
            response.sender = request.user
            response.save()
            
            # Mark enquiry as read if owner is responding
            if request.user == enquiry.property.owner:
                enquiry.is_read = True
                enquiry.save()
            
            messages.success(request, 'Response sent successfully!')
            return redirect('communications:enquiry_detail', enquiry_id=enquiry_id)
    else:
        form = EnquiryResponseForm()
    
    context = {
        'enquiry': enquiry,
        'responses': responses,
        'form': form,
    }
    return render(request, 'communications/enquiry_detail.html', context)

@login_required
def view_enquiries(request):
    if request.user.user_type != 'owner':
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    enquiries = Enquiry.objects.filter(property__owner=request.user).order_by('-created_at')
    
    # Mark all as read when owner views
    enquiries.update(is_read=True)
    
    paginator = Paginator(enquiries, 15)
    page_number = request.GET.get('page')
    enquiries = paginator.get_page(page_number)
    
    return render(request, 'communications/view_enquiries.html', {'enquiries': enquiries})

@login_required
def send_complaint(request, property_id):
    property_obj = get_object_or_404(Property, pk=property_id, is_approved=True)
    
    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.user = request.user
            complaint.property = property_obj
            complaint.save()
            messages.success(request, 'Your complaint has been submitted successfully!')
            return redirect('communications:my_complaints')
    else:
        form = ComplaintForm()
    
    context = {
        'form': form,
        'property': property_obj,
    }
    return render(request, 'communications/send_complaint.html', context)

@login_required
def my_complaints(request):
    if request.user.user_type not in ['buyer']:
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    complaints = Complaint.objects.filter(user=request.user).order_by('-created_at')
    
    paginator = Paginator(complaints, 10)
    page_number = request.GET.get('page')
    complaints = paginator.get_page(page_number)
    
    return render(request, 'communications/my_complaints.html', {'complaints': complaints})

@login_required
def view_complaints(request):
    if request.user.user_type != 'owner':
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    complaints = Complaint.objects.filter(property__owner=request.user).order_by('-created_at')
    
    paginator = Paginator(complaints, 15)
    page_number = request.GET.get('page')
    complaints = paginator.get_page(page_number)
    
    return render(request, 'communications/view_complaints.html', {'complaints': complaints})

@login_required
def update_complaint(request, complaint_id):
    complaint = get_object_or_404(Complaint, pk=complaint_id, property__owner=request.user)
    
    if request.method == 'POST':
        form = ComplaintResponseForm(request.POST, instance=complaint)
        if form.is_valid():
            form.save()
            messages.success(request, 'Complaint status updated successfully!')
            return redirect('communications:view_complaints')
    else:
        form = ComplaintResponseForm(instance=complaint)
    
    context = {
        'form': form,
        'complaint': complaint,
    }
    return render(request, 'communications/update_complaint.html', context)

@login_required
def send_feedback(request, property_id):
    property_obj = get_object_or_404(Property, pk=property_id, is_approved=True)
    
    # Check if user already gave feedback
    existing_feedback = Feedback.objects.filter(user=request.user, property=property_obj).first()
    if existing_feedback:
        messages.info(request, 'You have already provided feedback for this property.')
        return redirect('properties:detail', pk=property_id)
    
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user
            feedback.property = property_obj
            feedback.save()
            messages.success(request, 'Thank you for your feedback!')
            return redirect('properties:detail', pk=property_id)
    else:
        form = FeedbackForm()
    
    context = {
        'form': form,
        'property': property_obj,
    }
    return render(request, 'communications/send_feedback.html', context)

@login_required
def view_feedback(request):
    if request.user.user_type != 'owner':
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    feedback = Feedback.objects.filter(property__owner=request.user).order_by('-created_at')
    
    paginator = Paginator(feedback, 15)
    page_number = request.GET.get('page')
    feedback = paginator.get_page(page_number)
    
    return render(request, 'communications/view_feedback.html', {'feedback': feedback})
