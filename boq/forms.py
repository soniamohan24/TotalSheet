# boq/forms.py
from django import forms
from .models import CustomUser


class OTPRequestForm(forms.Form):
    identifier = forms.CharField(label="Phone Number or Email")

    def clean_identifier(self):
        identifier = self.cleaned_data["identifier"].strip()
        # Validate if it's an email or a phone number
        if "@" in identifier:
            # It's an email
            if not identifier:
                raise forms.ValidationError("Please enter a valid email address.")
        else:
            # It's a phone number
            if not identifier.isdigit():
                raise forms.ValidationError("Please enter a valid phone number.")
        return identifier
