from django import forms
from .models import ContactInquiry


class ContactForm(forms.ModelForm):
    """Form for contact inquiries."""
    
    class Meta:
        model = ContactInquiry
        fields = ['name', 'email', 'phone', 'inquiry_type', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Full Name',
                'required': True,
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Email Address',
                'required': True,
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Phone Number (Optional)',
            }),
            'inquiry_type': forms.Select(attrs={
                'class': 'form-select',
                'required': True,
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Please provide details about your inquiry...',
                'rows': 6,
                'required': True,
            }),
        }
