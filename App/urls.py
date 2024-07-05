from django.urls import path
from App import views


app_name = 'app'

urlpatterns = [
    path('', views.index, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register')
]