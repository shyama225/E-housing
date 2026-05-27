from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Property, PropertyImage

User = get_user_model()

class PropertyModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testowner',
            email='owner@example.com',
            password='testpass123',
            user_type='owner'
        )
        
        self.property = Property.objects.create(
            owner=self.user,
            title='Test Property',
            description='A beautiful test property',
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
    
    def test_property_creation(self):
        self.assertEqual(self.property.title, 'Test Property')
        self.assertEqual(self.property.owner, self.user)
        self.assertEqual(self.property.property_type, 'rent')
        self.assertFalse(self.property.is_approved)
        self.assertTrue(self.property.is_available)
    
    def test_property_str(self):
        expected = f"{self.property.title} - {self.property.get_property_type_display()}"
        self.assertEqual(str(self.property), expected)
    
    def test_get_absolute_url(self):
        url = self.property.get_absolute_url()
        self.assertIn(str(self.property.pk), url)
