from django.test import TestCase, Client
from django.urls import reverse
from .models import ContactInquiry, ContactConfiguration


class ContactFormTestCase(TestCase):
    """Test cases for contact form functionality."""

    def setUp(self):
        """Set up test data."""
        self.client = Client()
        self.contact_url = reverse('contact:contact')
        self.thank_you_url = reverse('contact:thank_you')
        
        # Create contact configuration
        self.config = ContactConfiguration.objects.create(
            admin_email='admin@example.com',
            admin_name='Test Admin',
            send_confirmation_email=True,
            enable_contact_form=True,
        )

    def test_contact_form_page_loads(self):
        """Test that contact form page loads successfully."""
        response = self.client.get(self.contact_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'modern/contact.html')

    def test_contact_form_submission(self):
        """Test successful contact form submission."""
        data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'phone': '+1234567890',
            'inquiry_type': 'service',
            'message': 'This is a test inquiry message.',
        }
        
        response = self.client.post(self.contact_url, data)
        self.assertEqual(response.status_code, 302)  # Redirect to thank you
        self.assertEqual(response.url, self.thank_you_url)
        
        # Verify inquiry was saved
        inquiry = ContactInquiry.objects.first()
        self.assertIsNotNone(inquiry)
        self.assertEqual(inquiry.name, 'John Doe')
        self.assertEqual(inquiry.email, 'john@example.com')

    def test_contact_form_required_fields(self):
        """Test that required fields are validated."""
        data = {
            'name': '',  # Required
            'email': '',  # Required
            'inquiry_type': 'question',
            'message': '',  # Required
        }
        
        response = self.client.post(self.contact_url, data)
        self.assertEqual(response.status_code, 200)  # Form re-renders with errors
        
        # Verify no inquiry was saved
        self.assertEqual(ContactInquiry.objects.count(), 0)

    def test_contact_form_disabled(self):
        """Test that contact form can be disabled."""
        self.config.enable_contact_form = False
        self.config.save()
        
        response = self.client.get(self.contact_url)
        self.assertEqual(response.status_code, 302)  # Redirect to homepage

    def test_thank_you_page(self):
        """Test thank you page loads correctly."""
        response = self.client.get(self.thank_you_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'modern/thank_you.html')

    def test_inquiry_status_tracking(self):
        """Test inquiry status tracking functionality."""
        inquiry = ContactInquiry.objects.create(
            name='Jane Doe',
            email='jane@example.com',
            inquiry_type='question',
            message='Testing status tracking.',
            status='new'
        )
        
        # Initially new
        self.assertEqual(inquiry.status, 'new')
        self.assertIsNone(inquiry.read_at)
        
        # Mark as read
        inquiry.mark_as_read()
        inquiry.refresh_from_db()
        self.assertEqual(inquiry.status, 'read')
        self.assertIsNotNone(inquiry.read_at)
