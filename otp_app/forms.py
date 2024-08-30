from django import forms

class OTPRequestForm(forms.Form):
    phone_number = forms.CharField(max_length=15, required=False, label='Phone Number')
    email = forms.EmailField(required=False, label='Email Address')


class OTPVerificationForm(forms.Form):
    otp = forms.CharField(max_length=6, min_length=6)