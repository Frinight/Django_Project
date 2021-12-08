from django.urls import path
from . import views

urlpatterns = [
    path('', views.receipt_list, name='home'),
    path('recipe/<int:pk>/', views.update_page, name='update_page'),
    path('del/<int:pk>/', views.del_receipt, name='del_receipt'),
    path('recipe/<int:pk>/del/<int:ing_pk>/', views.del_ing, name='del_ing'),
    path('new_recipe/', views.new_recipe, name='new_recipe'),
    path('new_recipe/add/', views.add_recipe, name='add_recipe'),
    path('recipe/<int:pk>/add/', views.add_product, name='add_product'),
    path('recipe/<int:pk>/ing/<int:ing_pk>/', views.update_ing_page, name='update_ing_page'),
    path('recipe/<int:pk>/ing/<int:ing_pk>/edit/', views.update_ing, name='update_ing'),
    path('recipe/<int:pk>/edit/', views.update_receipt, name="update_receipt"),
    path('my_receipts/', views.my_receipts, name='my_receipts'),
    path('signup/', views.signup, name="signup"),
    path('signup/add_user', views.add_user, name="add_user"),
]