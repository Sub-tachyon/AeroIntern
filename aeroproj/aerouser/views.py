from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password,check_password
from django.conf import settings
from django.core.mail import send_mail
import random,time
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.contrib import messages
from django.shortcuts import get_object_or_404
from .models import userdata, PasswordResetToken


def login(request):
     
     if request.method == 'POST':
        field1_data = request.POST.get('email')   
        field2_data = request.POST.get('password')
        
        if not userdata.objects.filter(email__iexact=field1_data).exists():
            error_message = "Email dosen't exists in the database."
            return render(request, "login.html", {'error_message': error_message})
            
        else:  
            user = userdata.objects.get(email=field1_data)
            stored_password = user.password
            name1=user.username
          
            if not check_password(field2_data,stored_password):
              error_message = "Wrong password"
              return render(request, "login.html", {'error_message': error_message})
            else:
             return render(request, "landing.html",{'error_message': name1})
     else:
        return render(request, "login.html")

def generate_otp():
    timestamp = str(int(time.time()))  
    random_number = str(random.randint(1000, 9999))  
    otp = timestamp[-4:] + random_number[-2:]  
    return otp

def signup(request):
    if request.method == 'POST':
        field1_data = request.POST.get('username')
        field2_data = request.POST.get('email')
        field3_data = request.POST.get('password')

        if userdata.objects.filter(email=field2_data).exists():
            error_message = "Email already exists in the database. Log in"
            return render(request, "signup.html", {'error_message': error_message})
        else:
            request.session['username'] = field1_data
            request.session['email'] = field2_data
            request.session['password'] = field3_data
            otp1 = generate_otp()
            request.session['otp'] = otp1
            subject = 'Welcome to Aerobiosys'
            message = f'Hi {field1_data}, thank you for signing up with Aerobiosys.'
            otp_message = f'Your OTP: {otp1}, please do not share.'
            combined_message = f'{message} {otp_message}'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [field2_data]
            send_mail(subject, combined_message, email_from, recipient_list)
            return render(request, "otp.html")
    else:
        return render(request, "signup.html")


def otp(request):
    error_message = None 
    user_name = request.session.get('username')
    user_email = request.session.get('email')
    user_password = request.session.get('password')
    user_otp = request.session.get('otp')

    if user_email and user_otp:
        if request.method == 'POST':
            entered_otp = request.POST.get('otp')
            try:
                if entered_otp == user_otp:
                    hashed_password = make_password(user_password)
                    new_entry = userdata(username=user_name, email=user_email, password=hashed_password)
                    new_entry.save()
                    return redirect("login")
                else:
                    error_message = "Incorrect OTP"
            except userdata.DoesNotExist:
                error_message = "User not found or email not available."
        else:
            return render(request, "otp.html", {'error_message': error_message})
    else:
        error_message = "User email or OTP not available in session."
    
    return render(request, "otp.html", {'error_message': error_message})


      
class PasswordResetTokenGeneratorApp(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            str(user.pk) + str(timestamp)
        )

password_reset_token = PasswordResetTokenGeneratorApp()


def forgot(request):
    if request.method == 'POST':
        field1_data = request.POST.get('email')
         
        try:
            user = userdata.objects.get(email=field1_data)
        except userdata.DoesNotExist:
            return render(request, 'forgot_password.html', {'error_message': 'User does not exist.'})
        
        token = password_reset_token.make_token(user)
        reset_link = f'http://localhost:8000/password_change/{token}' 

        subject = 'Reset Password'
        message = f'Click the link to reset your password: {reset_link}'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [field1_data]
        send_mail(subject, message, email_from, recipient_list)
        new_entry = PasswordResetToken(email=field1_data, token=token,)
        new_entry.save()
        return HttpResponse("Reset link sent")
    return render(request, 'forgot_password.html')
 

def password_reset(request, token):
    token_obj = get_object_or_404(PasswordResetToken, token=token)
    email = token_obj.email

    try:
        user = userdata.objects.get(email=email)
    except userdata.DoesNotExist:
        return HttpResponse("User not found")

    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_new_password = request.POST.get('confirm_new_password')

        if new_password == confirm_new_password:
            hashed_password = make_password(new_password)
            user.password = hashed_password
            user.save()
            token_obj.delete()  
            return HttpResponse("Password has been reset successfully")
        else:
            return render(request, 'reset_password.html', {'error_message': 'Password does not match'})

    return render(request, "reset_password.html")
