from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from . models import Customer
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def show_account(request):
    context={}
    if request.POST and 'register' in request.POST:
        context['register']=True
        try:
            username=request.POST.get('username')
            password=request.POST.get('password')
            email=request.POST.get('email')
            address=request.POST.get('address')
            phone=request.POST.get('phone')
            user_obj=User.objects.create_user(
                username=username,
                password=password,
                email=email
            )
            Customer.objects.create(
                user=user_obj,
                address=address,
                phone=phone
            )
            # return redirect('home')
            success_message="User Registered Successfully...!"
            messages.success(request, success_message)
        except Exception as e:
            error_message="Duplicate Username or Invalid Inputs"
            messages.error(request, error_message)

    if request.POST and 'login' in request.POST:
        context['register']=False
        username=request.POST.get('username')
        password=request.POST.get('password')
        user_obj=authenticate(username=username, password=password)
        if user_obj:
            login(request, user_obj)
            return redirect('home')
        else:
            error_message="Invalid Credentials"
            messages.error(request, error_message)

    return render(request, 'account.html', context)

def sign_out(request):
    logout(request)
    return redirect('home')
