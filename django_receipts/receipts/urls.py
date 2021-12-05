from django.urls import path
from . import views

urlpatterns = [
    path('', views.RecipeListView.as_view(), name='home'),
]