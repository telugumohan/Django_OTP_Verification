from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core.mail import send_mail
from .forms import OTPRequestForm, OTPVerificationForm
from .utils import send_otp_via_sms
import random
import smtplib

def generate_otp():
    return str(random.randint(100000, 999999))  # Generate a 6-digit OTP as a string


def send_otp_to_email(email, otp):
    try:
        send_mail(
            'Your OTP Code',
            f'Your OTP code is {otp}',
            'your-email@gmail.com',  # Sender email
            [email],  # Recipient email
            fail_silently=False,
        )
    except smtplib.SMTPException as e:
        print(f'SMTP error occurred: {e}')
    except Exception as e:
        print(f'Error sending email: {e}')
        return False
    return True

def send_otp(request):
    if request.method == 'POST':
        form = OTPRequestForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data.get('phone_number')
            email = form.cleaned_data.get('email')
            otp = generate_otp()  # Generate a single 6-digit OTP as a string

            success = True
            if phone_number:
                try:
                    send_otp_via_sms(phone_number, otp[:3])  # Send the first 3 digits to mobile
                except Exception as e:
                    print(f'Error sending SMS: {e}')
                    success = False

            if email:
                success &= send_otp_to_email(email, otp[3:])  # Send the last 3 digits to email

            if success:
                # Store the complete OTP in session
                request.session['otp'] = otp
                return redirect('verify_otp')  # Redirect to the OTP verification page
            else:
                return JsonResponse({"status": "error", "message": "Failed to send OTP"})
    else:
        form = OTPRequestForm()
    return render(request, 'otp_form.html', {'form': form})

def verify_otp(request):
    if request.method == 'POST':
        form = OTPVerificationForm(request.POST)
        if form.is_valid():
            user_otp = form.cleaned_data.get('otp')

            if user_otp == str(request.session.get('otp')):
                return redirect('success')  # Redirect to success page
            else:
                return render(request, 'verify_otp.html', {'form': form, 'error': 'Invalid OTP'})
    else:
        form = OTPVerificationForm()
    return render(request, 'verify_otp.html', {'form': form})




def success(request):
    return render(request, 'success.html')
