from django.core.files.utils import FileProxyMixin
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout,get_user_model
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes,force_text
from authentication.forms import UserLoginForm, UserRegistrationForm
from . tokens import generate_token
from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_decode

# from glamour.authentication import tokens



# Create your views here.
def home(request):
     return render(request,"authentication/index.html")

def signup(request):
    if request.method == "POST":
        username=request.POST['username']
        fname=request.POST['fname']
        lname=request.POST['lname']
        email=request.POST['email']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']

        if User.objects.filter(username=username):
            messages.error(request,'The username you entered is already in use')
            return redirect('home')
        
        if User.objects.filter(email=email):
            messages.error(request,'Email already exist')
            return redirect('home')

        if len(username)>15:
            messages.error(request,'username must be belo 15 characters')

        if pass1 != pass2:
            messages.error(request,'password did not match')

        if not username.isalnum():
            messages.error(request,'username must be Alpha-Numeric')

        myuser=User.objects.create_user(username,email,pass1)
        myuser.first_name= fname
        myuser.last_name= lname
        myuser.is_active=False

        myuser.save()

        messages.success(request,'Your account has been created successfully. We have sent you a confirmation email,please confirm your email in order to activate your account')

        # Thankyou email

        subject="Thank you for visiting our website"
        message="Hello" +myuser.first_name +'!!\n' +'Welcome to Style up'+'!!\n'+'We have also sent you a confirmation email,please confirm your email address to activate your account'
        from_email= settings.EMAIL_HOST_USER
        to_list=[myuser.email]
        send_mail(subject,message,from_email,to_list, fail_silently=True)
         
        #  Email address confirmation Email

        current_site=get_current_site(request)
        email_subject='confirm your email @ glamour -Django Login!!'
        message2=render_to_string('email_confirmation.html',{
            'name':myuser.first_name,
            'domain':current_site.domain,
            'uid':urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token':generate_token.make_token(myuser)
        })
        email=EmailMessage(
            email_subject,
            message2,
            settings.EMAIL_HOST_USER,
            [myuser.email],

        )
        email.fail_silently=True
        email.send()

        return redirect('signin')

    return render(request,"authentication/signup.html")

def signin(request):
    if request.method == 'POST':
        username=request.POST['username']
        pass1=request.POST['pass1']

        user= authenticate(username=username,password=pass1)

        if user is not None:
            login(request,user)
            fname=user.first_name
            return render(request,"authentication/index.html",{'fname':fname})
        else:
            messages.error(request,"Bad Credentials")

            return redirect('home')

    return render(request,"authentication/signin.html")

def signout(request):
    logout(request)
    messages.success(request,"logged out successfully!")
    return redirect('home')

def activate(request,uidb64,token):
    try:
        uid=force_text(urlsafe_base64_decode(uidb64))
        myuser=User.objects.get(pk=uid)
    except(TypeError,ValueError,OverflowError,User.DoesNotExist):
        myuser=None
    
    if myuser is not None and generate_token.check_token(myuser,token):
        myuser.is_active=True
        myuser.save()
        login(request,myuser)
        return redirect('home')
    else:
        return render(request,'activation_failed.html')

def login_view(request):
    next=request.GET.get('next')
    form= UserLoginForm(request.POST or None)
    if form.is_valid():
        username=form.cleaned_data.get('username')
        password=form.cleaned_data.get('password')
        user=authenticate(username=username,password=password)
        login(request,user)
        if next:
            return redirect(next)
        return redirect('/')

    context={
        'form':form,

    }
    return render(request,'login.html',context)

def register_view(request):
    next=request.GET.get('next')
    form= UserRegistrationForm(request.POST or None)
    if form.is_valid():
        user=form.save(commit=False)
        password=form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        new_user=authenticate(username=user.username,password=password)
        login(request,new_user)
        if next:
            return redirect(next)
        return redirect('/')

    context={
        'form':form,

    }
    return render(request,'signup.html',context)

def logout_view(request):
    logout(request)
    return redirect('/')

# from django.shortcuts import render
# from django.http.response import HttpResponse
# from django.shortcuts import redirect, render
# from django.contrib.auth.models import User
# from django.http import HttpResponse
# from django.contrib import messages
# from django.contrib.auth import authenticate, login, logout
# from fashion import settings
# from django.core.mail import send_mail
# from django.conf import settings
# from django.contrib.sites.shortcuts import get_current_site
# from django.template.loader import render_to_string
# from django.utils.http import urlsafe_base64_encode
# from django.utils.encoding import force_bytes,force_text
# from .tokens import generate_token
# from django.core.mail import EmailMessage
# from django.utils.http import urlsafe_base64_decode

# # from glamour.authentication import tokens



# # Create your views here.
# def home(request):
#      return render(request,"authentication/index.html")

# def signup(request):
#     if request.method == "POST":
#         username=request.POST['username']
#         fname=request.POST['fname']
#         lname=request.POST['lname']
#         email=request.POST['email']
#         pass1=request.POST['pass1']
#         pass2=request.POST['pass2']

#         if User.objects.filter(username=username):
#             messages.error(request,'Your account has been created successfully')
#             return redirect('home')
        
#         if User.objects.filter(email=email):
#             messages.error(request,'Email already exist')
#             return redirect('home')

#         if len(username)>15:
#             messages.error(request,'username must be belo 15 characters')

#         if pass1 != pass2:
#             messages.error(request,'password did not match')

#         if not username.isalnum():
#             messages.error(request,'username must be Alpha-Numeric')

#         myuser=User.objects.create_user(username,email,pass1)
#         myuser.first_name= fname
#         myuser.last_name= lname
#         myuser.is_active=False

#         myuser.save()
                    

#         messages.success(request,'Your account has been created successfully. We have sent you a confirmation email,please confirm your email in order to activate your account')

#         # Thankyou email

#         subject="Thank you for visiting our website"
#         message="Hello" +myuser.first_name +'!!\n' +'Welcome to Style up'+'!!\n'+'We have also sent you a confirmation email,please confirm your email address to activate your account'
#         from_email= settings.EMAIL_HOST_USER
#         to_list=[myuser.email]
#         send_mail(subject,message,from_email,to_list, fail_silently=True)
         
#         #  Email address confirmation Email

#         current_site=get_current_site(request)
#         email_subject='confirm your email @ glamour -Django Login!!'
#         message2=render_to_string('email_confirmation.html',{
#             'name':myuser.first_name,
#             'domain':current_site.domain,
#             'uid':urlsafe_base64_encode(force_bytes(myuser.pk)),
#             'token':generate_token.make_token(myuser)
#         })
#         email=EmailMessage(
#             email_subject,
#             message2,
#             settings.EMAIL_HOST_USER,
#             [myuser.email],

#         )
#         email.fail_silently=True
#         email.send()

#         return redirect('signin')

#     return render(request,"authentication/signup.html")

# def signin(request):
#     if request.method == 'POST':
#         username=request.POST['username']
#         pass1=request.POST['pass1']

#         user= authenticate(username=username,password=pass1)

#         if user is not None:
#             login(request,user)
#             fname=user.first_name
#             return render(request,"authentication/index.html",{'fname':fname})
#         else:
#             messages.error(request,"Bad Credentials")

#             return redirect('home')

#     return render(request,"authentication/signin.html")

# def signout(request):
#     logout(request)
#     messages.success(request,"logged out successfully!")
#     return redirect('home')

# def activate(request,uidb64,token):
#     try:
#         uid=force_text(urlsafe_base64_decode(uidb64))
#         myuser=User.objects.get(pk=uid)
#     except(TypeError,ValueError,OverflowError,User.DoesNotExist):
#         myuser=None
    
#     if myuser is not None and generate_token.check_token(myuser,token):
#         myuser.is_active=True
#         myuser.save()
#         login(request,myuser)
#         return redirect('home')
#     else:
#         return render(request,'activation_failed.html')
