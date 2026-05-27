from django.test import TestCase
from django.contrib.auth import get_user_model
from properties.models import Property
from .models import Enquiry, Complaint, Feedback

User = get_user_model()

class CommunicationModelTest(TestCase):
    def setUp(self):
        # Create users
        self.buyer = User.objects.create_user(
            username='buyer',
            email='buyer@example.com',
            password='testpass123',
            user_type='buyer'
        )
        
        self.owner = User.objects.create_user(
            username='owner',
            email='owner@example.com',
            password='testpass123',
            user_type='owner'
        )
        
        # Create property
        self.property = Property.objects.create(
            owner=self.owner,
            title='Test Property',
            description='A test property',
            property_type='rent',
            category='apartment',
            price=1500.00,
            bedrooms=2,
            bathrooms=1,
            area=1000,
            address='123 Test Street',
            city='Test City',
            state='Test State',
            pincode='12345'
        )
    
    def test_enquiry_creation(self):
        enquiry = Enquiry.objects.create(
            user=self.buyer,
            property=self.property,
            message='I am interested in this property',
            phone='+1234567890'
        )
        
        self.assertEqual(enquiry.user, self.buyer)
        self.assertEqual(enquiry.property, self.property)
        self.assertFalse(enquiry.is_read)
    
    def test_complaint_creation(self):
        complaint = Complaint.objects.create(
            user=self.buyer,
            property=self.property,
            subject='Test Complaint',
            description='This is a test complaint'
        )
        
        self.assertEqual(complaint.status, 'pending')
        self.assertEqual(complaint.user, self.buyer)
    
    def test_feedback_creation(self):
        feedback = Feedback.objects.create(
            user=self.buyer,
            property=self.property,
            rating=4,
            comment='Great property!'
        )
        
        self.assertEqual(feedback.rating, 4)
        self.assertEqual(feedback.user, self.buyer)
        self.assertEqual(feedback.property, self.property)
