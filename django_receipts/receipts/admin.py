from django.contrib import admin

# Register your models here.
from .models import Product, Ingredient, Recipe
 
admin.site.register(Product)
admin.site.register(Ingredient)
admin.site.register(Recipe)
