from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth.models import User
from tracker.models import Transaction
from .utils import add

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
            user = User.objects.create_user(username=username, email=email, password=password1)
            login(request, user)
            messages.success(request, 'Successfully registered.')
            return redirect('tracker:home')
        

    return render(request, 'auth/register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        if (not username) or (not password):
            messages.error(request, 'All field Required')
            return redirect('auth:login')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('auth:dashboard')
        else:
            messages.error(request, 'Username or Password not match')
            return redirect('auth:login')
    return render(request,'auth/login.html')


def logout_view(request):
    logout(request)
    return redirect('tracker:home')


@login_required
def dashboard_view(request):
    ''' 
    - Get the current user total income, expenses and debt.
    - Note: Transaction.objects.filter() -> return an instance of Transaction where some conditions were met. You must iterate it to get your value.
    - Get the transaction amout and save it in a list
    - Convert the amount to a float and get the sum
    - pass the sum to template

    '''
    user = request.user
    income_transaction = Transaction.objects.filter(user=user, choice='INCOME')
    expenses_transaction = Transaction.objects.filter(user=user, choice = 'EXPENSES')
    debt_transaction = Transaction.objects.filter(user=user, choice='DEBT')
    
    total_income = [ float(transaction.amount) for transaction in income_transaction ]
    total_expenses = [ float(transaction.amount) for transaction in expenses_transaction ]
    total_debt = [ float(transaction.amount) for transaction in debt_transaction ]

    if len(total_income) != 0:
        total_income = add(total_income)
    else:
        total_income = 0.00
        
    if len(total_expenses) != 0:
        total_expenses = add(total_expenses)
    else:
        total_expenses = 0.00

    if len(total_debt) != 0:
        total_debt = add(total_debt)
    else:
        total_debt = 0.00

    context = {
        'total_income': total_income,
        'total_expenses': total_expenses,
        'total_debt': total_debt,
    }
    
    return render(request, 'auth/dashboard.html', context)