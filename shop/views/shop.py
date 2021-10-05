from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login,logout,login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.hashers import make_password

# Create your views here.
def dashboard(request):
    return render(request,'dashboard.html')

