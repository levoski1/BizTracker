from django.http import HttpResponse
from django.shortcuts import render, redirect
from tracker.models import Transaction
from django.contrib import messages
from django.contrib.auth.decorators import login_required


# Create your views here.
def index(request):
    return render(request, 'tracker/home.html')


def create_view(request):
    if request.method == 'POST':
        description = request.POST.get('description').strip()
        amount = request.POST.get('amount').strip()
        choice = request.POST.get('category').strip()

        
        if request.user.is_authenticated:
            Transaction.objects.create(description=description,amount=amount,choice=choice, user=request.user)
            return redirect('tracker:home')
        else:
            return redirect('auth:login')

    return render(request, 'tracker/create_view.html')
