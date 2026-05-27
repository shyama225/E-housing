from django.urls import path
from . import views

app_name = 'properties'

urlpatterns = [
    path('', views.property_list, name='list'),
    path('<int:pk>/', views.property_detail, name='detail'),
    path('add/', views.add_property, name='add'),
    path('<int:pk>/edit/', views.edit_property, name='edit'),
    path('<int:pk>/delete/', views.delete_property, name='delete'),
    path('my-properties/', views.my_properties, name='my_properties'),
    path('<int:pk>/images/', views.manage_property_images, name='manage_images'),
    path('<int:pk>/images/<int:image_id>/delete/', views.delete_property_image, name='delete_image'),
    path('manage/', views.manage_properties, name='manage_properties'),
    path('<int:pk>/approve/', views.approve_property, name='approve'),
    path('<int:pk>/reject/', views.reject_property, name='reject'),
    path('<int:pk>/toggle-availability/', views.toggle_availability, name='toggle_availability'),
]
