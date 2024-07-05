from django.shortcuts import render, redirect
from django.http import HttpResponse
from App.forms import RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm

# Create your views here.
def index(request):
    return HttpResponse('This is Home Page')


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data.get('email')
            user.save()
            messages.success(request, 'You are successfully signed up')
            login(request, user)
            return redirect('app:home')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'Error in {field}: {error}')
    else:
        form = RegisterForm()
    return render(request, 'app/register.html', {"form": form})


# login view
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
#        print(f"Form Data: {request.POST}")
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
#            print(f"Username: {username}, Password: {password}")
            user = authenticate(request, username=username, password=password)
#            print(f"Authenticated User: {user}")
            if user is not None:
                login(request, user)
                messages.success(request, 'Login successful. Welcome to MedConnect!')
                return redirect('app:home')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
#            print("Form is not valid")
#            print(form.errors)
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'Error in {field} : {error}')
    else:
        form = AuthenticationForm()
    return render(request, 'app/login.html', {'form': form})
    

# logout view

def logout_view(request):
    logout(request)
    return redirect('home')
