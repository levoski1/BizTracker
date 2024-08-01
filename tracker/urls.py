from django.urls import path
from tracker import views


app_name = 'tracker'

urlpatterns = [
    path('', views.index, name='home'),
    path('transaction/create/', views.create_view, name='create'),
    path('transaction/read/', views.read_view,name='read'),
    path('transaction/update/<int:transaction_id>/', views.update_view, name='update')
]