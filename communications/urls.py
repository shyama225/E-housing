from django.urls import path
from . import views

app_name = 'communications'

urlpatterns = [
    # Enquiries
    path('enquiry/<int:property_id>/', views.send_enquiry, name='send_enquiry'),
    path('my-enquiries/', views.my_enquiries, name='my_enquiries'),
    path('enquiry-detail/<int:enquiry_id>/', views.enquiry_detail, name='enquiry_detail'),
    path('view-enquiries/', views.view_enquiries, name='view_enquiries'),
    
    # Complaints
    path('complaint/<int:property_id>/', views.send_complaint, name='send_complaint'),
    path('my-complaints/', views.my_complaints, name='my_complaints'),
    path('view-complaints/', views.view_complaints, name='view_complaints'),
    path('update-complaint/<int:complaint_id>/', views.update_complaint, name='update_complaint'),
    
    # Feedback
    path('feedback/<int:property_id>/', views.send_feedback, name='send_feedback'),
    path('view-feedback/', views.view_feedback, name='view_feedback'),
]
