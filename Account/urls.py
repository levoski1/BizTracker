from django.urls import path
from Account import views


app_name = 'account'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register')
]