from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Transaction(models.Model):
    INCOME = 'income'
    EXPENSES = 'expenses'
    DEBT = 'debt' 

    TYPE_CHOICES = [
        (INCOME, 'Income'),
        (EXPENSES, 'Expenses'),
        (DEBT, 'Debt'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    choice = models.CharField(max_length=10, choices=TYPE_CHOICES)

    def __str__(self):
        return self.user.username