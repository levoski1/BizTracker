from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from tracker.models import Transaction
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from tracker.utils import predict_category, preprocess_money
from django.http import JsonResponse


# Create your views here.
def index(request):

    return render(request, 'tracker/home.html')


def predict_view(request):
    '''
    Create a view to handle prediction requests
    '''
    if request.method == 'POST':
        input_text = request.POST.get('text')
        
        monetary_predition = preprocess_money(input_text)
        category = predict_category(input_text)
        print(category)
        prediction = {
            'input_text': input_text,
            'monetary_predition': monetary_predition,
            'category': category
        }
        if category == '' or  monetary_predition == '':
            return JsonResponse({'prediction': prediction})
        
        transact = Transaction(user=request.user, choice=category, amount=monetary_predition, text=input_text)
        transact.save()
        print(transact)
        
    return render(request, 'tracker/create_prediction.html')
    
   


def read_view(request):
    objects = Transaction.objects.all()
    return render(request, 'tracker/read_view.html', {'objects': objects})


def delete_view(request, transaction_id):
    transaction = get_object_or_404(Transaction, pk = transaction_id)
    #if request.user != transaction.user:
    #messages.error(request, 'You cannot delete this document')
    #return redirect('tracker:read')
    
    transaction.delete()
    return redirect('tracker:read')


