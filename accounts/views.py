from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth.models import User

# Create your views here.

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password1 = request.POST.get('password1', '').strip()
        password2 = request.POST.get('password2', '').strip()

        

        if (not username) or (not email) or (not password1) or (not password2):
            messages.error(request, 'All fields are required.')
            print('Data Required')
            return redirect('auth:register')
         
        elif User.objects.filter(email=email).exists():
            messages.error(request, f'Sorry! {email} Exist')
            print('Email exist')
            return redirect('auth:register')
        
        
        elif User.objects.filter(username=username).exists():
            messages.error(request, f'Sorry! {username} Exist')
            print('username exist')
            return redirect('auth:register')

        elif password1 != password2:
            messages.error(request, 'Password must match')
            print('password must match')
            return redirect('auth:register')
        
        
        elif len(password1) < 5:
            messages.error(request, 'Password must be at least five characters long.')
            return redirect('auth:register')

        else:
            User.objects.create_user(username=username, email=email, password=password1)
            messages.success(request, 'Successfully registered.')
            return redirect('tracker:home')
        

    return render(request, 'auth/register.html')

   


