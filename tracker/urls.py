from django.urls import path
from tracker import views


app_name = 'tracker'

urlpatterns = [
    path('', views.index, name='home'),
    path('create/', views.create_view, name='create'),
]