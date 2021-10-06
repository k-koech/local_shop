from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import string    
import random
from ..email import send_storeadmin_verification_email
from django.core.mail import send_mail
from shop.views.shop import dashboard
from ..models import Users
from django.contrib.auth.hashers import make_password

# Create your views here.
def index(request):
    return render(request,'auth/index.html')

""" LOGIN VIEW """
def signIn(request):
    if request.method=="POST":
        email=request.POST.get('email')
        password=request.POST.get('password')

        user= authenticate(email=email, password=password)
        if user is not None:
            login(request,user )
            return redirect(dashboard)
 
        else:
            messages.add_message(request, messages.ERROR, 'Invalid Credentials!')
            return redirect(signIn)

    else:
        return render(request,'auth/login.html')


"""STOREADMIN REGISTRATION"""
def register_storeadmin(request):
    if request.method=="POST":
        phone=request.POST.get('phone')
        email=request.POST.get('email')
        name=request.POST.get('name')
        username=request.POST.get('username')

        S = 10  
        ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k = S))  
        password=str(ran)

        username_exists=Users.objects.filter(username=username).count()
        email_exist=Users.objects.filter(email=email).count()

        if username_exists>0:
            messages.add_message(request, messages.ERROR, 'Username exists!')
            return redirect(dashboard)

        elif email_exist>0:
            messages.add_message(request, messages.ERROR, 'Email exist!')
            return redirect(dashboard)

        else:
            user = Users(name=name, email=email,username=username,phone_number=phone,is_active=False,is_storeadmin=True,   password=make_password(password))
            user.save()

            id=user.pk
            send_storeadmin_verification_email(id,name,password,email)

            messages.add_message(request, messages.SUCCESS, 'Registered successfully!')
            return redirect(dashboard)
     
    else:
        return redirect(dashboard)

"""ACTIVATEE STORE ADMIN"""
def activate_storeadmin(request, id):
    user=Users.objects.get(pk=id)
    user.is_active=True
    user.save()
    return redirect(signIn)


""" LOGOUT VIEW """
def signOut(request):
    logout(request)
    return redirect(signIn)
