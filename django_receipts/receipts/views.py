from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.urls.base import reverse
from .models import Recipe, Product, Ingredient
# from django.views.generic import ListView, DetailView
# from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy 
import itertools
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
            'id' : r.id,
            'name' : r.name,
            'cost' : r.total_cost,
            'weight' : r.total_weight,
            'description' : r.description,
            'components' : list(map(lambda x: str(x), list(r.ingredient_set.all()))),
        }
        receipts_data.append(receipt_data)

    context = { 'receipts_data' : receipts_data, } 
    return render(request, 'home.html', context)

def log(request):
    username = request.POST['login']
    print(username)
    password = request.POST['password']
    print(password)
    user = authenticate(username=username, password=password)
    context = {}
    if user is not None:
        if user.is_active:
            login(request, user)
            context['mes'] = "Авторизация прошла успешно"
            return render(request, 'home.html', context)
        else:
           context['mes'] =  "Такого пользователя не существует"
           return render(request, 'home.html', context)
    else:
        context['mes'] =  "Такого пользователя не существует"
        return render(request, 'home.html', context)

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

def signup(request):
    form = SignUpForm(request.POST)
    if form.is_valid():
        form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('home')
    context = {
        'form': form
    }
    return render(request, 'signup.html', context)

def add_user(request):
    form = SignUpForm(request.POST or None)
    # print(form.__dict__)
    # print(request.method)
    # print(form.is_valid())
    # print(list(itertools.chain(*form.errors)))
    # print(len(list(itertools.chain(*form.errors))))
    # print(form.non_field_errors)
    # print(form.cleaned_data.get('password'))
    if request.method == 'POST' and form.is_valid():
        form.save()
        return render(request, 'home.html', {'mes' : 'Пользователь успешно зарегистрирован', 'f':True})
    return render(request, 'signup.html', {'form': form, 'f':True})

def my_receipts(request):
    if request.user.is_authenticated:
        print(request.user.username)
        receipts = Recipe.objects.filter(author__username=request.user.username)
        receipts_data = []
        for r in receipts:
            receipt_data = {
                'id' : r.id,
                'name' : r.name,
                'cost' : r.total_cost,
                'weight' : r.total_weight,
                'description' : r.description,
                'components' : list(map(lambda x: str(x), list(r.ingredient_set.all()))),
            }
            receipts_data.append(receipt_data)
        context = { 'receipts_data' : receipts_data, } 
        return render(request, 'home.html', context)
    else:
        context = {'mes' : "Вы не авторизованы"}
        return render(request, 'home.html', context)

def update_page(request, pk):
    receipt = Recipe.objects.get(id=pk)
    form = RecipeCreationForm(initial={'name': receipt.name, 'total_weight': receipt.total_weight, 'description': receipt.description})
    print("------------------------------------------------------------------------------------------------------------------------")
    print(form.is_valid())
    # if form.is_valid():
    #     # form.save()
    #     # username = form.cleaned_data.get('username')
    #     # password = form.cleaned_data.get('password')
    #     # user = authenticate(username=username, password=password)
    #     # login(request, user)
    #     return redirect('home')
    receipt = Recipe.objects.get(id=pk)
    context = {
        'form': form, 
        'pk': pk, 
        'receipt': receipt,
        'components' : list(map(lambda x: str(x), list(receipt.ingredient_set.all()))),
    }
    return render(request, 'edit_recipe.html', context)

def update_receipt(request, pk):
    return HttpResponse('111111111')
# class LoginUser(LoginView):
#     form_class = LoginUserForm
#     template_name = 'home.html'

#     def get_success_url(self):
#         return reverse_lazy('home')
