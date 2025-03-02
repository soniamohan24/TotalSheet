from django import forms
from django.contrib.auth.forms import UserCreationForm
from boq.models import CustomUser


class PhoneNumberForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["phone_number", "email"]


class OTPRequestForm(forms.Form):
    otp = forms.CharField(max_length=6, required=True)


class PasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=True)
