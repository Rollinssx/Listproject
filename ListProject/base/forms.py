from django.contrib.auth.forms import forms
from django.contrib.auth.models import models
from .models import ToDoItem, ToDoList, User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class ToDoItemForm(forms.ModelForm):
    class Meta:
        model = ToDoItem
        fields = ['description', 'completed']
        widgets = {'completed': forms.CheckboxInput(attrs={'class': 'custom-checkbox'})}


class ToDoListForm(forms.ModelForm):
    class Meta:
        model = ToDoList
        fields = ['list_name']


class EditToDoListForm(forms.ModelForm):
    class Meta:
        model = ToDoList
        fields = ['list_name']  # Allow only the title to be edited


class EditToDoItemForm(forms.ModelForm):
    class Meta:
        model = ToDoItem
        fields = ['description', 'completed']  # Allow description and completion status to be edited


class MyLoginForm(AuthenticationForm):
    username = forms.EmailField(widget=(forms.EmailInput(attrs={'class': 'custom-field'})))
    password = forms.CharField(widget=(forms.PasswordInput(attrs={'class': 'custom-field'})))

    class Meta:
        model = User
        fields = ['username', 'password']


class MyRegisterForm(UserCreationForm):
    first_name = forms.CharField(widget=(forms.TextInput(attrs={'class': 'custom-field'})))
    last_name = forms.CharField(widget=(forms.TextInput(attrs={'class': 'custom-field'})))
    email = forms.EmailField(widget=(forms.EmailInput(attrs={'class': 'custom-field'})))
    username = forms.CharField(widget=(forms.TextInput(attrs={'class': 'custom-field'})))
    password1 = forms.CharField(widget=(forms.PasswordInput(attrs={'class': 'custom-field'})))
    password2 = forms.CharField(widget=(forms.PasswordInput(attrs={'class': 'custom-field'})))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


