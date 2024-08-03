from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
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


def update_view(request, transaction_id):
    transaction = get_object_or_404(Transaction, pk=transaction_id)
    if request.method == 'POST':
        if request.user.id != transaction.user.id:
            messages.error(request, 'Sorry! You cannot update this.')
            return redirect('tracker:read')
        transaction.description = request.POST.get('description').strip()
        transaction.amount = request.POST.get('amount').strip()
        transaction.choice = request.POST.get('choice').strip()
        transaction.user = request.user
        transaction.save()
        return redirect('tracker:read')
        
    return render(request, 'tracker/update_view.html')


def read_view(request):
    objects = Transaction.objects.all()
    return render(request, 'tracker/read_view.html', {'objects': objects})


def delete_view(request, transaction_id):
    transaction = get_object_or_404(Transaction, pk = transaction_id)
    if request.user != transaction.user:
        messages.error(request, 'You cannot delete this document')
        return redirect('tracker:read')
    transaction.delete()
    return redirect('tracker:read')