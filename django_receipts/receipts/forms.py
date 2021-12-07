from django import forms
from .models import Recipe, Ingredient, Product
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product 
        fields = ['name']
        widgets = {
            'name' : forms.TextInput(attrs=
            {
                'class' : 'input', 
                'required':'',
                'name':'name',
                'id':'name',
                'type':'text',
                'placeholder' : 'Наименование продукта'
            })}

class IngredientCreationForm(forms.ModelForm):

    product_name = forms.CharField(max_length=255, label=False)
    class Meta:
        model = Ingredient
        fields = ('product_name', 'qty', 'unit', 'cost',)
        widgets = {
            'product_name': forms.TextInput(attrs=
            {
                'class': 'form-input',
                'required':'',
                'name':'product_name',
                'id':'product_name',
                'type':'text',
                'placeholder':'Ингредиент',
            }),
            'qty': forms.NumberInput(attrs=
            {
                'class': 'form-input',
                'required':'',
                'name':'qty',
                'id':'qty',
                'type':'number',
                'placeholder':'Количество',
            }),
            'unit': forms.TextInput(attrs=
            {
                'class': 'form-input',
                'required':'',
                'name':'unit',
                'id':'unit',
                'type':'text',
                'placeholder':'Единица измерения',
            }),
            'cost': forms.NumberInput(attrs=
            {
                'class': 'form-input',
                'required':'',
                'name':'cost',
                'id':'cost',
                'type':'number',
                'placeholder':'Стоимость',
            })
        }

class RecipeCreationForm(forms.ModelForm):

    class Meta:
        model = Recipe
        fields = ('name', 'total_weight', 'description',)
        widgets = {
            'name': forms.TextInput(attrs=
            {
                'class': 'form-input',
                'required':'',
                'name':'name',
                'id':'name',
                'type':'text',
                'placeholder':'Наименование',
            }),
            'total_weight': forms.NumberInput(attrs=
            {
                'class': 'form-input',
                'required':'',
                'name':'total_weight',
                'id':'total_weight',
                'type':'number',
                'placeholder':'Общий вес',
            }),
            'description': forms.Textarea(attrs=
            {
                'class': 'form-input',
                'required':'',
                'name':'description',
                'id':'description',
                'type':'text',
                'placeholder':'Описание',
            })
        }
    # def save(self, commit=True):
    #     rec = super(RecipeCreationForm, self).save(commit=False)
    #     rec.name = self.cleaned_data['name']
    #     rec.total_weight = self.cleaned_data['total_weight']
    #     rec.total_cost = 309
    #     rec.description = self.cleaned_data['description']

    #     if commit:
    #         rec.save()

    #     return rec

class SignUpForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-input',
            'required':'',
            'name':'username',
            'id':'username',
            'type':'text',
            'placeholder':'Username',
            'maxlength': '16',
            'minlength': '6',
            })
        self.fields['email'].widget.attrs.update({
            'class': 'form-input',
            'required':'',
            'name':'email',
            'id':'email',
            'type':'email',
            'placeholder':'Email',
            })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-input',
            'required':'',
            'name':'password1',
            'id':'password1',
            'type':'password',
            'placeholder':'Password',
            'maxlength':'22', 
            'minlength':'8'
            })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-input',
            'required':'',
            'name':'password2',
            'id':'password2',
            'type':'password',
            'placeholder':'Repeat password',
            'maxlength':'22', 
            'minlength':'8'
            })

    username = forms.CharField(max_length=20, label=False)
    email = forms.EmailField(max_length=100)
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.set_password(self.cleaned_data["password1"])

        if commit:
            user.save()

        return user

# class LoginUserForm(AuthenticationForm):
#     username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
#     password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))