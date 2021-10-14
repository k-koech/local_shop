from django.http import request
from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import string    
import random
from ..email import send_storeadmin_verification_email,clerk_registration_email
from django.core.mail import send_mail
from shop.views.shop import dashboard
from ..models import Users
from django.contrib.auth.hashers import check_password, make_password

# Create your views here.
def index(request):
    return render(request,'auth/index.html')

""" LOGIN VIEW """
def signIn(request):        
    if request.method=="POST":
        email=request.POST.get('email')
        password=request.POST.get('password')
       
        user_exists=Users.objects.filter(email=email).count()
        if user_exists>0:
            user=Users.objects.get(email=email)
           
            if user.status==0:
                messages.add_message(request, messages.ERROR, 'Your account has been suspended! Please contact the admin')
                return redirect(signIn)
            
            elif user.status==2:
                messages.add_message(request, messages.ERROR, 'Your account has been banned! Please contact the admin')
                return redirect(signIn)
            
            elif user.is_active==False :
                messages.add_message(request, messages.ERROR, 'Please activate your account!')
                return redirect(signIn)
            
            
            else:
                user= authenticate(email=email, password=password)
                if user is not None:
                    login(request,user )
                    return redirect(dashboard)
        
                else:
                    messages.add_message(request, messages.ERROR, 'Invalid Credentials!')
                    return redirect(signIn)
        else:
            messages.add_message(request, messages.ERROR, 'User do not exist!')
            return redirect(signIn)

    else:
        return render(request,'auth/login.html')


"""STOREADMIN REGISTRATION"""
@login_required(login_url='/login')
def register_storeadmin(request):
    if request.method=="POST":
        phone=request.POST.get('phone')
        email=request.POST.get('email')
        name=request.POST.get('name')
        username=request.POST.get('username')
        store_name=request.POST.get('store_name')
        
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
            user = Users(name=name, email=email,username=username,phone_number=phone,is_active=False,is_storeadmin=True,store=store_name, password=make_password(password))
            user.save()

            id=user.pk
            send_storeadmin_verification_email(id,name,password,email)

            messages.add_message(request, messages.SUCCESS, 'Registered successfully!')
            return redirect(dashboard)
     
    else:
        return redirect(dashboard)

"""ACTIVATEE STORE ADMIN"""
def activate_storeadmin(request, id):
    if request.method=="POST":
        user=Users.objects.get(pk=id)
        user.is_active=True
        user.save()
        messages.add_message(request,messages.SUCCESS,"Activated successfully!")
        return redirect(signIn)
    else:
        return render(request, "email/storeadmin_activationpage.html")

'''ADD CLERK'''
@login_required(login_url='/login')
def addclerk(request):
    if request.method=="POST":
        name=request.POST.get('name')
        phone=request.POST.get('phone')
        email=request.POST.get('email')
        username=request.POST.get('username')
        name=request.POST.get('name')
        clerkname=Users.objects.filter(username=username).count()
        clerkmail=Users.objects.filter(email=email).count()
        if clerkname>0:
            messages.add_message(request,messages.ERROR,'The username is already taken')
            return redirect('dashboard')
        elif clerkmail>0:
            messages.add_message(request,messages.ERROR, 'The email is already in use')
            return redirect('dashboard')
    
        else:
            password=str(''.join(random.choices(string.ascii_uppercase + string.digits, k = 10)))
            clerk=Users(name=name,username=username,phone_number=phone,email=email,is_superuser=False,is_active=False,is_storeadmin=False,store=request.user.store, password=make_password(password))
            clerk.save()
            id=clerk.pk
            messages.add_message(request,messages.SUCCESS,"Clerk registration was successful")
            clerk_registration_email(id,name,password,email)
    return redirect('dashboard')

@login_required(login_url='/login')
def activate_clerk(request,id):
    ''' activate the clerk '''
    if request.method=="POST":
        user=Users.objects.get(pk=id)
        user.is_active=True
        user.save()
        messages.add_message(request,messages.SUCCESS,"Activated successfully!")
        return redirect(signIn)
    else:
        return render(request, "email/clerk_acivationpage.html")

"""PROFILE"""
@login_required(login_url='/login')
def profile(request):
    return render(request, "profile.html")

""" LOGOUT VIEW """
@login_required(login_url='/login')
def signOut(request):
    logout(request)
    return redirect(signIn)

"""UPDATE PASSWORD"""
@login_required(login_url='/login')
def updatepassword(request):
    old_password=request.POST.get('old_password')
    password=request.POST.get('password')
    confirm_password=request.POST.get('confirm_password')

    user=Users.objects.get(id=request.user.id)
    if user.check_password('{}'.format(old_password)) == False:
        messages.add_message(request,messages.ERROR,"Old password is wrong!")
        return redirect(profile)
    elif len(password)<4 or len(confirm_password)<4:
        messages.add_message(request,messages.ERROR,"Password too short!")
        return redirect(profile)
    elif password!=confirm_password:
        messages.add_message(request,messages.ERROR,"Password doesn't match!")
        return redirect(profile)
    else:
        user=Users.objects.get(id=request.user.id)
        user.password=make_password(password)
        user.save()
        messages.add_message(request,messages.SUCCESS,"Password updated successfully!")
        return redirect(profile)

"""UPDATE PROFILE"""
@login_required(login_url='/login')
def update_profile(request):
    if request.method=="POST":
        phone=request.POST.get('phone')
        username=request.POST.get('username')

        username_exists=Users.objects.filter(username=username).count()

        if username_exists>0 and username!=request.user.username:
            messages.add_message(request, messages.ERROR, 'Username taken!')
            return redirect(profile)

        elif len(phone)<10 or len(phone)>13:
            messages.add_message(request, messages.ERROR, 'Phone number should be atleast 10 characters!')
            return redirect(profile)

        else:
            user=Users.objects.get(id=request.user.id)
            user.username=username
            user.phone_number=phone
            user.save()
            messages.add_message(request,messages.SUCCESS,"Profile updated successfully!")
            return redirect(profile)
    


"""UPDATE PROFILE PHOTO"""
@login_required(login_url='/login')
def update_profilephoto(request):
    if request.method=="POST":
        profile_photo=request.FILES.get('profile_photo')

        user=Users.objects.get(id=request.user.id)
        user.profile_photo=profile_photo
        user.save()
        messages.add_message(request,messages.SUCCESS,"Profile photo updated successfully!")
        return redirect(profile)
@login_required(login_url='/login')
def adminact_clerk(request,id):
    Users.objects.filter(id=id).update(is_active=True, status=1 )
    messages.add_message(request,messages.SUCCESS,'Changes Saved successfully!')
    return redirect(dashboard)

@login_required(login_url='/login')
def admindeact_clerk(request,id):
    Users.objects.filter(id=id).update(is_active=False, status=0)
    messages.add_message(request,messages.SUCCESS,'Changes Saved successfully!')
    return redirect(dashboard)

@login_required(login_url='/login')
def update_clerk(request,id):
    
    name=request.POST.get('username')
    mail=request.POST.get('mail'),
    phone=request.POST.get('phone')
    email="".join(mail)
    mailcount=Users.objects.filter(email=email).count()
    usercount=Users.objects.filter(username=name).count()
    user=Users.objects.filter(email=email).first()
    if mailcount>1:
        response={'response':'The email alreday exist'}
        return JsonResponse(response)
    elif usercount>0 and user.username!=name:
        response={'response':'The username is already taken'}
        return JsonResponse(response)
    else:
        Users.objects.filter(id=id).update(username=name,email=email,phone_number=phone)
        response={'response':'success'}
        return JsonResponse(response)
@login_required(login_url='/login')

def delete_clerk(request,id):
    
    Users.objects.filter(pk=id).delete()
    
    return redirect(dashboard)
    
    