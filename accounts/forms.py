# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import Profile
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm # Import AuthenticationForm
from django.contrib.auth.models import User

class RegistrationForm(UserCreationForm):
    # ... (RegistrationForm remains the same)
    email = forms.EmailField(required=True, help_text='Required. Inform a valid email address.', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))


    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "first_name", "last_name") # Ensure username is also styled if needed
        widgets = { # Add this if you didn't customize fields individually above
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            # email, first_name, last_name already handled above by redefining fields.
            # If you didn't redefine, add them here.
        }
    # ... (clean_email method remains the same)
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("This email address is already in use. Please use a different one.")
        return email


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        # No need for widgets here if fields are redefined above with widgets

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'address_line_1', 'address_line_2', 'city', 'state_province_region', 'postal_zip_code', 'country', 'phone_number']
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'address_line_1': forms.TextInput(attrs={'class': 'form-control'}),
            'address_line_2': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state_province_region': forms.TextInput(attrs={'class': 'form-control'}),
            'postal_zip_code': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}), # Consider a Select widget if you have predefined countries
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'type': 'tel'}),
            # 'profile_picture': forms.ClearableFileInput(attrs={'class': 'form-control'}), # If you add ImageField
        }

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control form-control-lg', # Added form-control-lg for a slightly larger input
        'placeholder': 'Username',
        'autofocus': True
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control form-control-lg',
        'placeholder': 'Password'
    }))

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        # Add the new field to the list
        fields = ['bio', 'profile_picture_url', 'address_line_1', 'address_line_2', 'city', 'state_province_region', 'postal_zip_code', 'country', 'phone_number']
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            # Add a widget for the new URL field
            'profile_picture_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://example.com/image.png'}),
            'address_line_1': forms.TextInput(attrs={'class': 'form-control'}),
            'address_line_2': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state_province_region': forms.TextInput(attrs={'class': 'form-control'}),
            'postal_zip_code': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'type': 'tel'}),
        }