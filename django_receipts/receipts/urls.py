from django.urls import path
from . import views

urlpatterns = [
    path('', views.receipt_list, name='home'),
]