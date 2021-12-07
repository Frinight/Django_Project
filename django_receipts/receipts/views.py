from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.urls.base import reverse
from .models import Recipe, Product, Ingredient
from django.db.models import Sum
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
    if request.user.is_authenticated:
        receipt = Recipe.objects.get(id=pk)
        form_prod = ProductForm()
        form = RecipeCreationForm(initial={'name': receipt.name, 'total_weight': receipt.total_weight, 'description': receipt.description})
        # print("------------------------------------------------------------------------------------------------------------------------")
        # print(form.is_valid())
        # print(form.errors)
        # print(form.non_field_errors)
        # if form.is_valid():
        #     # form.save()
        #     # username = form.cleaned_data.get('username')
        #     # password = form.cleaned_data.get('password')
        #     # user = authenticate(username=username, password=password)
        #     # login(request, user)
        #     return redirect('home')
        context = {
            'form': form, 
            'form_prod': form_prod, 
            'pk': pk, 
            'receipt': receipt,
            'components' : receipt.ingredient_set.all(),
            'sum' : receipt.ingredient_set.all().aggregate(Sum('cost'))['cost__sum'],
        }
        return render(request, 'edit_recipe.html', context)
    else:
        context = {'mes' : "Вы не авторизованы"}
        return render(request, 'home.html', context)

def update_receipt(request, pk):
    form = RecipeCreationForm(request.POST)
    # print("------------------------------------------------------------------------------------------------------------------------")
    # print(form.is_valid())
    # print(form.errors)
    # print(form.non_field_errors)
    if request.method == 'POST' and form.is_valid():
        name = form.cleaned_data.get('name')
        total_weight = form.cleaned_data.get('total_weight')
        description = form.cleaned_data.get('description')
        receipt = Recipe.objects.get(id=pk)
        receipt.sum = receipt.ingredient_set.all().aggregate(Sum('cost'))['cost__sum']
        receipt.name = name
        receipt.total_weight = total_weight
        receipt.description = description
        receipt.save()
        return render(request, 'home.html')
    return render(request, 'edit_recipe.html', {'form': form})

def update_ing_page(request, pk, ing_pk):
    ing = Ingredient.objects.get(id=ing_pk)
    form = IngredientCreationForm(initial={'product_name': ing.product.name, 'qty': ing.qty, 'unit': ing.unit, 'cost': ing.cost})
    context = {
            'form': form, 
            'pk': pk, 
            'ing_pk': ing_pk,
            'ing': ing,
        }
    return render(request, 'edit_ing.html', context)

def update_ing(request, pk, ing_pk):
    form = IngredientCreationForm(request.POST)
    if request.method == 'POST' and form.is_valid():
        product_name = form.cleaned_data.get('product_name')
        qty = form.cleaned_data.get('qty')
        unit = form.cleaned_data.get('unit')
        cost = form.cleaned_data.get('cost')
        ing = Ingredient.objects.get(id=ing_pk)
        # print(ing.product.name)
        prod, f = Product.objects.get_or_create(name=product_name)
        ing.product_id = prod.id
        ing.qty = qty
        ing.unit = unit
        ing.cost = cost
        ing.save()
        return update_page(request, pk)
    return render(request, 'edit_ing.html', {'form': form, 'f':True})

def add_product(request, pk):
    form = ProductForm(request.POST)
    print("------------------------------------------------------------------------------------------------------------------------")
    print(form.is_valid())
    print(form.errors)
    if request.method == 'POST' and form.is_valid():
        product_name = form.cleaned_data.get('name')
        prod, f = Product.objects.get_or_create(name=product_name)
        ing = Ingredient.objects.create(recipe_id=pk, product_id=prod.id, qty=1, unit="г", cost=1)
        print(ing)
        return update_page(request, pk)
    return render(request, 'home.html')

    #     receipt.sum = receipt.ingredient_set.all().aggregate(Sum('cost'))['cost__sum']
    #     receipt.name = name
    #     receipt.total_weight = total_weight
    #     receipt.description = description
    #     receipt.save()
    #     return render(request, 'home.html')
    # return render(request, 'edit_recipe.html', {'form': form})
# class LoginUser(LoginView):
#     form_class = LoginUserForm
#     template_name = 'home.html'

#     def get_success_url(self):
#         return reverse_lazy('home')
