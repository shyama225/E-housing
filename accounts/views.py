from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Q
from .forms import CustomUserCreationForm, CustomAuthenticationForm, ProfileForm
from .models import Profile
from properties.models import Property
from communications.models import Enquiry, Complaint, Feedback

User = get_user_model()

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Registration successful! Please wait for admin approval.')
            return redirect('accounts:login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_approved or user.user_type == 'admin':
                    login(request, user)
                    
                    # Redirect based on user type
                    if user.user_type == 'admin':
                        return redirect('accounts:admin_dashboard')
                    elif user.user_type == 'owner':
                        return redirect('accounts:owner_dashboard')
                    else:
                        return redirect('accounts:user_dashboard')
                else:
                    messages.error(request, 'Your account is pending approval.')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')

@login_required
def dashboard_view(request):
    user = request.user
    if user.user_type == 'admin':
        return redirect('accounts:admin_dashboard')
    elif user.user_type == 'owner':
        return redirect('accounts:owner_dashboard')
    else:
        return redirect('accounts:user_dashboard')

@login_required
def user_dashboard(request):
    if request.user.user_type != 'buyer':
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    properties = Property.objects.filter(is_approved=True)
    my_enquiries = Enquiry.objects.filter(user=request.user).order_by('-created_at')[:5]
    my_complaints = Complaint.objects.filter(user=request.user).order_by('-created_at')[:5]
    
    context = {
        'properties': properties,
        'my_enquiries': my_enquiries,
        'my_complaints': my_complaints,
    }
    return render(request, 'accounts/user_dashboard.html', context)

@login_required
def owner_dashboard(request):
    if request.user.user_type != 'owner':
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    my_properties = Property.objects.filter(owner=request.user)
    new_enquiries = Enquiry.objects.filter(property__owner=request.user, is_read=False).count()
    new_complaints = Complaint.objects.filter(property__owner=request.user, status='pending').count()
    total_feedback = Feedback.objects.filter(property__owner=request.user).count()
    
    context = {
        'my_properties': my_properties,
        'new_enquiries': new_enquiries,
        'new_complaints': new_complaints,
        'total_feedback': total_feedback,
    }
    return render(request, 'accounts/owner_dashboard.html', context)

def is_admin(user):
    return user.user_type == 'admin'

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    total_users = User.objects.exclude(user_type='admin').count()
    pending_users = User.objects.filter(is_approved=False).exclude(user_type='admin').count()
    total_properties = Property.objects.count()
    pending_properties = Property.objects.filter(is_approved=False).count()
    
    context = {
        'total_users': total_users,
        'pending_users': pending_users,
        'total_properties': total_properties,
        'pending_properties': pending_properties,
    }
    return render(request, 'accounts/admin_dashboard.html', context)

@login_required
@user_passes_test(is_admin)
def manage_users(request):
    users = User.objects.exclude(user_type='admin').order_by('-date_joined')
    return render(request, 'accounts/manage_users.html', {'users': users})

@login_required
@user_passes_test(is_admin)
def approve_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.is_approved = True
    user.save()
    messages.success(request, f'User {user.username} has been approved.')
    return redirect('accounts:manage_users')

@login_required
@user_passes_test(is_admin)
def reject_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    messages.success(request, f'User has been rejected and deleted.')
    return redirect('accounts:manage_users')

@login_required
def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('accounts:profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'accounts/profile.html', {'form': form, 'profile': profile})