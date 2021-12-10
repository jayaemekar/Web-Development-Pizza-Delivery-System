from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *
from django.contrib.auth import authenticate

CHOICES = [
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Other', 'Other'),
]

class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'First Name', 'class': 'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Last Name', 'class': 'form-control'}))
    gender = forms.ChoiceField(choices=CHOICES)

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'gender', 'phone', 'password1', 'password2']
        widgets = {
            'email' : forms.EmailInput(attrs = {'placeholder': 'Email', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['gender'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].widget.attrs['class'] = 'form-control'




class UserLoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)  # to hide the password-field-value while typing

    class Meta:
        model = CustomUser
        fields = ['email', 'password']

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            
            # Raise auth-error where this form gets rendered
            if not authenticate(email=email, password=password):
                raise forms.ValidationError("Invalid Credentials! Please insert correct email & password.")

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['placeholder'] = 'Email Address'
        self.fields['password'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['placeholder'] = 'Enter Password'