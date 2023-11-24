from django.shortcuts import render
from django.http import HttpResponse
from .models import userdata
from django.contrib.auth.hashers import make_password,check_password
from django.conf import settings
from django.core.mail import send_mail
import random,time
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail



def login(request):
     error_message = None 
     if request.method == 'POST':
        field1_data = request.POST.get('email')   
        field2_data = request.POST.get('password')
        
        if not userdata.objects.filter(email__iexact=field1_data).exists():
            error_message = "Email dosen't exists in the database."
            print("email no exsist")
            return render(request, "login.html", {'error_message': error_message})
            
        else:  
            user = userdata.objects.get(email=field1_data)
            stored_password = user.password
          
            if not check_password(field2_data,stored_password):
              error_message = "wrong password"
              return render(request, "login.html", {'error_message': error_message})
            else:
             return HttpResponse("login successful")
     else:
        return render(request, "login.html", {'error_message': error_message})

def generate_otp():
    timestamp = str(int(time.time()))  
    random_number = str(random.randint(1000, 9999))  
    otp = timestamp[-4:] + random_number[-2:]  
    return otp

def signup(request):
    error_message = None 
    if request.method == 'POST':
         
        field1_data = request.POST.get('username')  
        field2_data = request.POST.get('email')   
        field3_data = request.POST.get('password')
         
       
        if userdata.objects.filter(email=field2_data).exists():
            error_message = "Email already exists in the database."
            return render(request, "signup.html", {'error_message': error_message})
        else:
            request.session['email'] = field2_data 
            otp1 = generate_otp()
            hashed_password = make_password(field3_data)
            new_entry = userdata(username=field1_data, email=field2_data, password=hashed_password,otp=otp1)
            new_entry.save()
            subject = 'welcome to Aerobiosys'
            message = f'Hi {field1_data}, thank you for signing up with Aerobiosys.'
            otp_message = f'Your Otp: {otp1},please do not share.'
            combined_message = f'{message} {otp_message}'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [field2_data]
            send_mail( subject, combined_message,email_from, recipient_list )
            return render(request, "otp.html") 
    else:
        return render(request, "signup.html", {'error_message': error_message}) 

      
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

        return HttpResponse("Reset link sent")
    return render(request, 'forgot_password.html')

def otp(request):
    error_message = None 
    user_email = request.session.get('email')

    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        
        if user_email:
            try:
                user_data = userdata.objects.get(email=user_email)
                stored_otp = user_data.otp
                
                if entered_otp == str(stored_otp):
                    return HttpResponse("OTP verified successfully")
                else:
                    return render(request,"otp.html")
            except userdata.DoesNotExist:
                error_message = "User not found or email not available."
        else:
            error_message = "User email not available in session."
    
    return render(request, "otp.html", {'error_message': error_message})

 

def password_reset(request, token):
    try:
        
        user = userdata.objects.get(pk=token.split('-')[0])
    except (TypeError, ValueError, OverflowError, userdata.DoesNotExist):
        return HttpResponse("user not found")
    
    if password_reset_token.check_token(user, token):
        if request.method == 'POST':
            new_password = request.POST.get('password')
            confirm_new_password = request.POST.get('confirm_password')
            
            if new_password == confirm_new_password:
                user.set_password(new_password)
                user.save()
                
                return HttpResponse("Password Changed, please Login")
            else:
                return render(request, 'password_change.html', {'error_message': 'Passwords do not match.'})
        else:
            return render(request, 'password_change.html')
    else:
        return HttpResponse("Error")