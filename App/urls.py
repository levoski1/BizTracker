from django.urls import path
from App import views


app_name = 'app'

urlpatterns = [
    path('', views.index, name='home'),
]