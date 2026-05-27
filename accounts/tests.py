from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Profile

User = get_user_model()

class UserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            user_type='buyer'
        )
    
    def test_user_creation(self):
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertEqual(self.user.user_type, 'buyer')
        self.assertFalse(self.user.is_approved)
    
    def test_profile_creation(self):
        self.assertTrue(hasattr(self.user, 'profile'))
        self.assertIsInstance(self.user.profile, Profile)
    
    def test_dashboard_url(self):
        # Test different user types dashboard URLs
        buyer_url = self.user.get_dashboard_url()
        self.assertIn('user', buyer_url)
        
        self.user.user_type = 'owner'
        owner_url = self.user.get_dashboard_url()
        self.assertIn('owner', owner_url)
        
        self.user.user_type = 'admin'
        admin_url = self.user.get_dashboard_url()
        self.assertIn('admin', admin_url)
