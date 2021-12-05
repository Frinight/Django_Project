from django.shortcuts import render
from django.http import HttpResponse
from .models import Recipe, Product, Ingredient
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy 

# Create your views here.
# def index(request):
#     return HttpResponse()

class RecipeListView(ListView):
    model = Recipe
    template_name = 'home.html'
    context_object_name = 'all_receipts_list'