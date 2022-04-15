import datetime
import time

from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from .form import UserCreationForm
from .models import User, OTPLog, News, Visitor, Buy
from .email import email_message
from django.contrib import auth
from django.core.mail import send_mail
import math, random


def login_view(request):
    context = {
        'title': 'Sign In'
    }
    error = ''
    if request.method == "POST":
        print('hi')
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(email, password)
        user = authenticate(request, email=email, password=password)

        if user is not None:

            login(request, user)
            return redirect("societyapp:dashboard")
        else:
            error = "Invalid credentials!"
    return render(request, 'login.html', {'error': error})


def generateOTP():
    digits = "0123456789"
    OTP = ""
    for i in range(4):
        OTP += digits[math.floor(random.random() * 10)]
    return OTP


def reg_otp_view(request):
    email_message(request.session['email'], 'Registration OTP', request.session['message'])
    print('Hi i am', request.session['email'])
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
            active_user = User.objects.get(email=request.session['email'])
            print(active_user)
            active_user.is_active = True
            active_user.save()
            user = authenticate(request, email=request.session['email'], password=request.session['password'])

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
                user = User.objects.create_user(request.POST['email'], password=request.POST['password1'],
                                                flat_no=request.POST['flat_no'], mobile_no=request.POST['mobile_no'],
                                                first_name=request.POST['fname'], last_name=request.POST['lname'])
                try:
                    otp = OTPLog.objects.get(email=request.POST.get('email')).otp
                except:
                    otp = random.randint(100000, 999999)
                    OTPLog.objects.create(email=request.POST.get('email'), otp=otp).save()

                message = 'Your OTP is: ' + str(otp)

                print(request.POST.get('email'))
                request.session['otp'] = otp
                request.session['message'] = message

                request.session['email'] = request.POST.get('email')
                request.session['password'] = request.POST['password1']
                request.session['email'] = request.POST.get('email')
                print('your password is', request.POST['password1'])
                return redirect("societyapp:otp")
        else:
            return render(request, 'signup.html', {'error': 'Password does not match!'})
    else:
        return render(request, 'signup.html')
    return render(request, 'signup.html')


def dashboard(request):
    context = {}
    news = News.objects.all()
    visitor = Visitor.objects.all()
    context.__setitem__('newss', news)
    context.__setitem__('visitors', visitor)
    return render(request, 'dashboard.html', context=context)


def resetpassword(request):
    if request.method == "POST":
        email = request.POST.get('email')
        try:
            User.objects.get(email=email)
            email_message(email, 'Reset Link', 'http://127.0.0.1:9981/setpassword')
            error = 'Please Check You Email'
            return render(request, 'reset.html', {'error': error})
        except User.DoesNotExist:
            error = 'Please enter valid email Thank You'
            return render(request, 'reset.html', {'error': error})
    return render(request, 'reset.html')


def setpassword(request):
    if request.method == "POST":
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            user.set_password(request.POST.get('password'))
            return redirect('societyapp:login')
        except User.DoesNotExist:
            error = 'User Does Not Exist Please enter valid email Thank You'
            return render(request, 'setpassword.html', {'error': error})
    return render(request, 'setpassword.html')


def logout(request):
    auth.logout(request)
    return redirect('societyapp:dashboard')


def add_news(request):
    if request.method == "POST":
        title = request.POST.get('title')
        news = request.POST.get('news')
        date = datetime.datetime.now()
        new_news = News(title=title, containt=news, date=date)
        new_news.save()
        success = 'News Added'
        return render(request, 'add_news.html', {'success': success})
    return render(request, 'add_news.html')


def profile(request):
    return render(request, 'user_profile.html')


def add_visitor(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        gender = request.POST.get('gender')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        print(mobile)
        message = request.POST.get('massage')
        print(message)
        visitor = Visitor(name=first_name + " " + last_name, gender=gender, mobile=mobile, message=message)
        visitor.save()
        print(visitor.__dict__)
        success = 'Visitor Added'
        return render(request, 'add_visitor.html', {'success': success})

    return render(request, 'add_visitor.html')


def reslist(request):
    user = User.objects.all()
    return render(request, 'resident_list.html', {'users': user})


def buy_rent(request):
    if request.method == 'POST':
        types = request.POST.get('type')
        if types:
            request.session['type'] = types
            return render(request, 'rent_buy.html', {'types': types})
        type = request.session['type']
        name = request.POST.get('name')
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')
        member = request.POST.get('member')
        amount = request.POST.get('amnt')
        bank = request.POST.get('bank')
        if bank is None:
            bank = 'Cash'
        furnish = request.POST.get('furnished')
        if furnish is None:
            furnish = 'Not'
        fac = ''
        if request.POST.get('fac1'):
            fac = fac + ' ' + request.POST.get('fac1')
        if request.POST.get('fac2'):
            fac = fac + ' ' + request.POST.get('fac2')
        if request.POST.get('fac3'):
            fac = fac + ' ' + request.POST.get('fac3')
        message = request.POST.get('message')
        buy = Buy(name=name, mobile=mobile, type=type, amount=amount, members=member, message=message, furnish=furnish,
                  bank=bank, email=email)
        message = "Someone will contact you soon"
        print(message)
        render(request, 'rent_buy.html', {'message': message})
    return render(request, 'rent_buy.html')
