from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from .form import UserCreationForm
from .models import User, OTPLog
from .email import email_message
from django.contrib import auth
from django.core.mail import send_mail
import math, random


def login_view(request):
    context = {
        'title': 'Sign In'
    }

    if request.method == "POST":
        print('hi')
        print(request.POST.all())
        username = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("/")
        else:
            context['login_error'] = "Invalid credentials!"
    return render(request, 'user/login.html', context)


def generateOTP():
    digits = "0123456789"
    OTP = ""
    for i in range(4):
        OTP += digits[math.floor(random.random() * 10)]
    return OTP


def send_otp(request):
    email = User.objects.get(email=request.POST['email'])
    o = generateOTP()
    htmlgen = '<p>Your OTP is <strong>' + o + '</strong></p>'
    send_mail('OTP request', o, '<gmail id>', [email], fail_silently=False, html_message=htmlgen)
    return HttpResponse(o)

def reg_otp_view(request):
    print('Hi i am',request.session['email'])
    context = {
        'title': 'OTP Verification',
        'email': request.session['email']
    }

    if request.POST == "GET":
        print("Resend OTP")

    print(OTPLog.objects.get(email=request.session['email']).otp)
    if request.method == "POST":
        otp = OTPLog.objects.get(email=request.session['email'])
        if int(request.POST.get('otp')) == int(otp.otp):
            User.objects.create_user(
                username=request.session['email'],
                email=request.session['email'],
                password=request.session['password']
            )

            user = authenticate(request, username=request.session['email'], password=request.session['password'])

            if user is not None:
                login(request, user)
            return redirect('societyapp:login')
        else:
            context['error'] = "Wrong OTP"
    return render(request, 'otp.html', context)

def index(request):
    if request.method == "POST":
        if request.POST['password1'] == request.POST['password2']:
            try:
                User.objects.get(email=request.POST['email'])
                return render(request, 'signup.html', {'error': 'Email is already taken!'})
            except User.DoesNotExist:
                user = User.objects.create_user(request.POST['email'], password=request.POST['password1'])
                try:
                    otp = OTPLog.objects.get(email=request.POST.get('email')).otp
                except:
                    otp = random.randint(100000, 999999)
                    OTPLog.objects.create(email=request.POST.get('email'), otp=otp).save()

                message = 'Your OTP is: ' + str(otp)
                email_message(request.POST.get('email'), 'Registration OTP', message)
                print(request.POST.get('email'))
                request.session['email'] = request.POST.get('email')
                request.session['password'] = request.POST['password1']
                request.session['email'] = request.POST.get('email')
                return redirect("societyapp:otp")
        else:
            return render(request, 'signup.html', {'error': 'Password does not match!'})
    else:
        return render(request, 'signup.html')
    return render(request, 'signup.html')


