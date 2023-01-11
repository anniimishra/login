
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from login import settings
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site


# Create your views here.
def home(request):
    return render(request,"authentication/index.html")

def signup(request):
    if request.method=="POST":
        username=request.POST.get('username')
        firstname=request.POST.get('firstname')
        lastname=request.POST.get('lastname')
        password=request.POST.get('Password')
        Confirm_Passward=request.POST.get('Confirm')
        email=request.POST.get('Email')

        if User.objects.filter(username=username):
            messages.error(request,"username already exist")
            

        if User.objects.filter(email=email):
            messages.error(request,"email already exist")
            return redirect('home')

        if len(username)>10:
            messages.error(request,"usernsme size limit exceded")
            

        if password!=Confirm_Passward:
            messages.error(request,"both password are not matching")
            

        if not username.isalnum():
            messages.error(request,"alfabets and numerical are used in username")

        myuser=User.objects.create_user(username=username,email=email,password=password)
        myuser.first_name=firstname
        myuser.last_name=lastname
        myuser.is_active=False
        myuser.save()

        messages.success(request,"Your Account Opened Sucessfully and we have sent you an confirmation mail")


        #email
        subject="welcome to our page"
        message="hello"+myuser.first_name+"\nthank you for login into my website"
        from_email=settings.EMAIL_HOST_USER
        to_list=[myuser.email]
        send_mail(subject,message,from_email,to_list, fail_silently=True)

        return redirect('signin')


    return render(request,"authentication/signup.html")

def signin(request):
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('Password')

        user=authenticate(username=username,password=password)
        # user=User.objects.filter(username=username).first()


        if user is not None:
            login(request,user)
            fname=user.first_name
            return render(request,"authentication/index.html",{'fname':fname})

        else:
            messages.error(request,"wrong username or password")
            return redirect('home')

    

    return render(request,"authentication/signin.html")

def signout(request):
    logout(request)
    messages.success(request,"Logged out successfully")
    return redirect("home")
