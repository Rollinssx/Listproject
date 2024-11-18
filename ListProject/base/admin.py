from django.contrib import admin
from .models import User, ToDoList, ToDoItem

# Register your models here.
admin.site.register(User)
admin.site.register(ToDoList)
admin.site.register(ToDoItem)

