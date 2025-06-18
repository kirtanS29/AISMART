from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken')
            return redirect('signup')
        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        return redirect('home')  # assuming 'home' route exists
    return render(request, 'accounts/signup.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login')
    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')
#otp authrntication
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.core.mail import send_mail
from .models import EmailOTP
import random

def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        # Create inactive user
        user = User.objects.create_user(username=username, email=email, password=password)
        user.is_active = False
        user.save()

        # Generate and store OTP
        otp = str(random.randint(100000, 999999))
        EmailOTP.objects.create(user=user, otp_code=otp)

        # Send OTP to email
        send_mail(
            'Your SmartAI OTP',
            f'Your OTP is: {otp}',
            'yourproject@gmail.com',  # From email (must match settings.py)
            [email],
            fail_silently=False,
        )

        request.session['user_id'] = user.id
        return redirect('verify_otp')  # URL name for verify_otp view

    return render(request, 'accounts/signup.html')


def verify_otp_view(request):
    if request.method == 'POST':
        entered_otp = request.POST['otp']
        user_id = request.session.get('user_id')
        user = User.objects.get(id=user_id)
        otp_obj = EmailOTP.objects.get(user=user)

        if otp_obj.otp_code == entered_otp:
            user.is_active = True
            user.save()
            otp_obj.delete()  # Clean up used OTP
            return redirect('login')  # Redirect to login
        else:
            return render(request, 'accounts/verify_otp.html', {'error': 'Invalid OTP'})

    return render(request, 'accounts/verify_otp.html')
