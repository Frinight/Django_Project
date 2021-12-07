from django import forms
from .models import Recipe, Ingredient
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

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
                'placeholder':'Описнание',
            })
        }

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