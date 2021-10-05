from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login,logout,login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.hashers import make_password

# Create your views here.
def index(request):
    return render(request,'auth/index.html')

""" LOGIN VIEW """
def signIn(request):
    return render(request,'auth/login.html')

""" LOGOUT VIEW """
def signOut(request):
    logout(request)
    return redirect(index)
