from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth import logout, login, authenticate
# from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.urls.base import reverse
from .models import Recipe, Product, Ingredient
# from django.views.generic import ListView, DetailView
# from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy 
from .forms import *

# Create your views here.
# def index(request):
#     return HttpResponse()

# class RecipeListView(ListView):
#     model = Recipe
#     template_name = 'home.html'
#     context_object_name = 'all_receipts_list'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['components'] = [list(map(lambda x: str(x), list(recipe.ingredient_set.all())))
#                                     for recipe in Recipe.objects.all()]

#         return context

def receipt_list(request):

    receipts = Recipe.objects.all()
    receipts_data = []
    for r in receipts:
        receipt_data = {
            'name' : r.name,
            'cost' : r.total_cost,
            'weight' : r.total_weight,
            'description' : r.description,
            'components' : list(map(lambda x: str(x), list(r.ingredient_set.all()))),
        }
        receipts_data.append(receipt_data)

    context = {
        'receipts_data' : receipts_data, 
    }

    return render(request, 'home.html', context)

def log(request):
    username = request.POST['login']
    print(username)
    password = request.POST['password']
    print(password)
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return HttpResponseRedirect('/')
        else:
           context = {'mes' : "Нет такого пользователя"}
           return redirect(reverse('home'), context)
    else:
        context = {'mes' : "Нет такого пользователя"}
        return redirect(reverse('home'), context)

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

# class LoginUser(LoginView):
#     form_class = LoginUserForm
#     template_name = 'home.html'

#     def get_success_url(self):
#         return reverse_lazy('home')
