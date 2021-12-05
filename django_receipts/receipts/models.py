from django.db import models

# Create your models here.
class Recipe(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True, )
    name = models.CharField(max_length=255)
    total_cost = models.DecimalField(max_digits=8, decimal_places=2,)
    total_weight = models.PositiveIntegerField()
    description = models.TextField()

    def __str__(self):
        return "Рецепт \"" + self.name + "\"" + " опубликован пользователем " + self.author.username

class Product(models.Model):
    name = models.CharField(max_length=255, unique=True, db_index=True)
    def __str__(self):
        return self.name

class Ingredient(models.Model):
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete = models.CASCADE)
    qty = models.PositiveSmallIntegerField()
    unit = models.CharField(max_length=15)
    cost = models.DecimalField(max_digits=8, decimal_places=2,)
    def __str__(self):
        return self.recipe.name + ": Ингредиент \"" + self.product.name + "\"" + " в количестве " + str(self.qty) + " " + self.unit

