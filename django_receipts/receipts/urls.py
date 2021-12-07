from django.urls import path
from . import views

urlpatterns = [
    path('', views.receipt_list, name='home'),
    path('recipe/<int:pk>/', views.update_page, name='update_page'),
    path('recipe/<int:pk>/edit/', views.update_receipt, name="update_receipt"),
    path('my_receipts/', views.my_receipts, name='my_receipts'),
    path('signup/', views.signup, name="signup"),
    path('signup/add_user', views.add_user, name="add_user"),
]