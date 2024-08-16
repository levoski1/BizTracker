from django.urls import path
from tracker import views


app_name = 'tracker'

urlpatterns = [
    path('', views.index, name='home'),
    path('transaction/predict/', views.predict_view, name='predict'),
    path('transaction/read/', views.read_view,name='read'),
    path('transaction/delete/<int:transaction_id>/', views.delete_view, name='delete'),

    
]