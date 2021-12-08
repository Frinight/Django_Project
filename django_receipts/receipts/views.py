from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.urls.base import reverse
from .models import Recipe, Product, Ingredient, Note
from django.db.models import Sum
from django.urls import reverse_lazy 
from itertools import groupby
from .forms import *

def receipt_list(request):
    """
    Для выведения списка рецептов на начальной странице
    """
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
            'note': False if not request.user.is_authenticated or Note.objects.filter(author__username=request.user.username, recipe_id=r.id).count() == 0 else True,
        }
        receipts_data.append(receipt_data)

    context = { 'receipts_data' : receipts_data, } 
    return render(request, 'home.html', context)

def log(request):
    """
    Авторизация пользователей
    """
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
    """
    Выход из своей учетной записи
    """
    logout(request)
    return HttpResponseRedirect('/')

def signup(request):
    """
    Отображение страницы регистрации пользователей
    """
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
    """
    Непосредственное добавление нового пользователя в случае валидности данных формуляра
    """
    form = SignUpForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return render(request, 'home.html', {'mes' : 'Пользователь успешно зарегистрирован'})
    return render(request, 'signup.html', {'form': form, 'f':True})

def my_receipts(request):
    """
    Отображение списка рецептов, добавленных текущим пользователем
    """
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

def update_page(request, pk, con={}):
    """
    Страница, содержащая формы изменения рецепта
    """
    if request.user.is_authenticated:
        receipt = Recipe.objects.get(id=pk)
        form_prod = ProductForm()
        form = RecipeCreationForm(initial={'name': receipt.name, 'total_weight': receipt.total_weight, 'description': receipt.description})
        context = {
            'form': form, 
            'form_prod': form_prod, 
            'pk': pk, 
            'receipt': receipt,
            'components' : receipt.ingredient_set.all(),
            'sum' : receipt.ingredient_set.all().aggregate(Sum('cost'))['cost__sum'],
        }
        context.update(con)
        return render(request, 'edit_recipe.html', context)
    else:
        context = {'mes' : "Вы не авторизованы"}
        return render(request, 'home.html', context)

def update_receipt(request, pk):
    """
    Обновление данных о рецепте
    """
    form = RecipeCreationForm(request.POST)
    if request.method == 'POST' and form.is_valid():
        name = form.cleaned_data.get('name')
        total_weight = form.cleaned_data.get('total_weight')
        description = form.cleaned_data.get('description')
        receipt = Recipe.objects.get(id=pk)
        receipt.total_cost = receipt.ingredient_set.all().aggregate(Sum('cost'))['cost__sum'] if receipt.ingredient_set.count() else 0
        receipt.name = name
        receipt.total_weight = total_weight
        receipt.description = description
        receipt.save()
        return render(request, 'home.html')
    return render(request, 'edit_recipe.html', {'form': form})

def update_ing_page(request, pk, ing_pk):
    """
    Отображение страницы изменения выбранного ингридиента
    """
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
    """
    Обновление данных об ингридиенте
    """
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
        receipt = Recipe.objects.get(id=pk)
        receipt.total_cost = receipt.ingredient_set.all().aggregate(Sum('cost'))['cost__sum']
        receipt.save()
        return update_page(request, pk)
    return render(request, 'edit_ing.html', {'form': form, 'f':True})

def add_product(request, pk):
    """
    Добавление новой позиции в список ингридиентов выбранного рецепта
    """
    form = ProductForm(request.POST)
    # print("------------------------------------------------------------------------------------------------------------------------")
    # print(form.is_valid())
    # print(form.errors)
    if request.method == 'POST' and form.is_valid():
        product_name = form.cleaned_data.get('name')
        prod, f = Product.objects.get_or_create(name=product_name)
        ing = Ingredient.objects.create(recipe_id=pk, product_id=prod.id, qty=1, unit="г", cost=0)
        # print(ing)
        return update_page(request, pk)
    return update_page(request, pk, con={'f': True, 'errors': form.errors})

def new_recipe(request):
    """
    Отображение страницы добавления нового рецепта
    """
    if request.user.is_authenticated:
        form = RecipeCreationForm()
        context = {
            'form': form, 
        }
        return render(request, 'add_recipe.html', context)
    else:
        context = {'mes' : "Вы не авторизованы"}
        return render(request, 'home.html', context)

def add_recipe(request):
    """
    Непосредственное добавление нового рецепта
    """
    form = RecipeCreationForm(request.POST)
    if request.method == 'POST' and form.is_valid():
        name = form.cleaned_data.get('name')
        total_weight = form.cleaned_data.get('total_weight')
        description = form.cleaned_data.get('description')
        receipt = Recipe.objects.create(name=name, total_weight=total_weight, description=description, total_cost=0)
        return update_page(request, receipt.id)
    return render(request, 'add_recipe.html', {'form': form, 'f':True})

def del_receipt(request, pk):
    """
    Удаление выбранного рецепта
    """
    if request.user.is_authenticated:
        Recipe.objects.get(id=pk).delete() 
        return receipt_list(request)
    else:
        context = {'mes' : "Вы не авторизованы"}
        return render(request, 'home.html', context)

def del_ing(request, pk, ing_pk):
    """
    Удаление выбранного ингридиента
    """
    ing = Ingredient.objects.get(id=ing_pk).delete()
    return update_page(request, pk)

def note(request, pk):
    """
    Cоздание/удаление пометки понравившегося рецепта
    """
    if request.user.is_authenticated:
        is_exist = Note.objects.filter(author__username=request.user.username, recipe_id=pk).count()
        if is_exist == 0:
            Note.objects.create(author_id=request.user.id, recipe_id=pk)
        else:
            Note.objects.get(author_id=request.user.id, recipe_id=pk).delete()
        return receipt_list(request)
    else:
        context = {'mes' : "Вы не авторизованы"}
        return render(request, 'home.html', context)

def chosen(request):
    """
    Вывод общего аггрегированного списка продуктов, необходимых для приготовления выбранных блюд
    """
    if request.user.is_authenticated:
        res = []
        w = 0
        c = 0
        total = 0
        receipts_id = [obj.recipe_id for obj in Note.objects.filter(author__username=request.user.username)]
        ingredients_id = []
        for obj in Recipe.objects.all():
            if obj.id in receipts_id:
                ingredients_id.extend(obj.ingredient_set.in_bulk())
        d =  [{'name': obj.product.name, 'qty': obj.qty, 'unit': obj.unit, 'cost': obj.cost} for obj in Ingredient.objects.all() if obj.id in ingredients_id]
        # print(d)
        d = sorted(d, key=grouper)
        for key, group_items in groupby(d, key=grouper):
            # print('Key: %s' % key)
            dict_elem = {'name': key}
            group_items= sorted(group_items, key=subgrouper)
            for subkey, subgroup_items in groupby(group_items, key=subgrouper): 
                # print('Item: %s' % subkey)
                w = 0
                c = 0
                for subitem in subgroup_items:
                    w += subitem['qty']
                    c += subitem['cost']
                    # print('Item: %s' % subitem)
                if dict_elem.get('unit', None) is None:
                    dict_elem['unit'] = str(w) + " " + subkey
                    dict_elem['cost'] = c
                    total += c
                else:
                    dict_elem['unit'] += " + " + str(w) + " " + subkey
                    dict_elem['cost'] += c
                    total += c
            res.append(dict_elem)
        print(res)
        return render(request, 'chosen.html', {'res': res, 'total': total})
    else:
        context = {'mes' : "Вы не авторизованы"}
        return render(request, 'home.html', context)

def grouper(item):
        """Будем использовать эту функцию для группировки сортировки."""
        return item['name']

def subgrouper(item):
        """Будем использовать эту функцию для группировки сортировки."""
        return item['unit']