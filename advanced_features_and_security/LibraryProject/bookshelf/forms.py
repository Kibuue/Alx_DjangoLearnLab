"""
Secure forms with built-in validation and sanitization.
Django forms automatically protect against SQL injection by using parameterized queries.
They also provide input validation and sanitization.
"""

from django import forms
from .models import Book
from django.core.exceptions import ValidationError
import re

class BookForm(forms.ModelForm):
    """
    Secure form for creating and editing books.
    Uses Django's ModelForm which automatically:
    - Sanitizes input
    - Prevents SQL injection
    - Validates data types
    """
    
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter book title',
                'maxlength': '200',  # Limit input length
            }),
            'author': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter author name',
                'maxlength': '100',
            }),
            'publication_year': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter publication year',
                'min': '1000',  # Prevent invalid years
                'max': '2100',
            }),
        }
    
    def clean_title(self):
        """
        Custom validation for title field.
        Sanitizes and validates the title.
        """
        title = self.cleaned_data.get('title')
        
        # Remove any potentially dangerous characters
        # This is an extra layer; Django already handles most XSS
        if not title or len(title.strip()) == 0:
            raise ValidationError("Title cannot be empty.")
        
        # Check for excessively long input (DoS prevention)
        if len(title) > 200:
            raise ValidationError("Title is too long (max 200 characters).")
        
        return title.strip()
    
    def clean_author(self):
        """
        Custom validation for author field.
        """
        author = self.cleaned_data.get('author')
        
        if not author or len(author.strip()) == 0:
            raise ValidationError("Author name cannot be empty.")
        
        if len(author) > 100:
            raise ValidationError("Author name is too long (max 100 characters).")
        
        return author.strip()
    
    def clean_publication_year(self):
        """
        Validate publication year is reasonable.
        """
        year = self.cleaned_data.get('publication_year')
        
        if year < 1000 or year > 2100:
            raise ValidationError("Please enter a valid publication year.")
        
        return year


class ExampleForm(forms.Form):
    """
    Example form demonstrating various security practices.
    """
    
    # Text input with validation
    name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your name'
        })
    )
    
    # Email field with built-in validation
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'your.email@example.com'
        })
    )
    
    # Textarea with character limit
    message = forms.CharField(
        max_length=1000,
        required=True,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your message',
            'rows': 5
        })
    )
    
    def clean_name(self):
        """
        Sanitize name input.
        """
        name = self.cleaned_data.get('name')
        
        # Only allow letters, spaces, hyphens, and apostrophes
        if not re.match(r"^[a-zA-Z\s\-']+$", name):
            raise ValidationError("Name can only contain letters, spaces, hyphens, and apostrophes.")
        
        return name.strip()
    
    def clean_message(self):
        """
        Sanitize message content.
        """
        message = self.cleaned_data.get('message')
        
        # Remove leading/trailing whitespace
        message = message.strip()
        
        # Check for minimum length
        if len(message) < 10:
            raise ValidationError("Message must be at least 10 characters long.")
        
        return message