from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth import authenticate, login, logout
from .forms import MyRegisterForm, MyLoginForm, ToDoItemForm, ToDoListForm, ToDoList, ToDoItem
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import EditToDoListForm, EditToDoItemForm
from django.forms import modelformset_factory
# Create your views here.


def home(request):
    return render(request, 'base/home.html')


def logout_page(request):
    logout(request)
    messages.info(request, 'Logged out successfully')
    return redirect('home')


def register_page(request):
    page = 'register'
    form = MyRegisterForm()
    if request.method == 'POST':
        form = MyRegisterForm(request.POST)
        form.save()

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Logged in successfully')
                return redirect('home')
    context = {'form': form, 'page': page}
    return render(request, 'base/login_register.html', context)


def login_page(request):
    page = 'login'
    form = MyLoginForm()  # Initialize the form for GET requests

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = MyLoginForm(request, data=request.POST or None)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            print(f"Attempting login with email: {username} and password: {password}")

            user = authenticate(request, username=username, password=password)
            if user is not None:
                user.save()
                login(request, user)
                messages.success(request, 'Logged in successfully')
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password')  # Provide feedback on invalid credentials

    context = {'form': form, 'page': page}
    print(f'form errors: {form.errors}')
    return render(request, 'base/login_register.html', context)


def list_detail(request, pk):
    # Retrieve the specific to-do list
    page = 'list_details'

    to_do_list = get_object_or_404(ToDoList, id=pk, user=request.user)
    items = ToDoItem.objects.filter(list=to_do_list)  # Get items within the list

    context = {
        'to_do_list': to_do_list,
        'items': items,
        'page': page,
    }
    return render(request, 'base/list_details.html', context)


def update_item(request, pk):
    page = 'list_details'
    item = get_object_or_404(ToDoItem, id=pk)

    # Check if the request method is POST to update the 'completed' field
    if request.method == 'POST':
        item.completed = 'completed' in request.POST  # Update based on checkbox state
        item.save()

    # Load all items for the associated to-do list
    to_do_list = item.list
    items = to_do_list.items.all()  # Fetch all items in the current list

    context = {'to_do_list': to_do_list, 'items': items, 'page': page}
    return render(request, 'base/list_details.html', context)


def list_view(request):
    # Get all lists for the logged-in user
    page = 'list_view'

    user_lists = ToDoList.objects.filter(user=request.user)
    context = {
        'user_lists': user_lists,
        'page': page,
    }
    return render(request, 'base/my_tasks.html', context)


@login_required
def create_to_do_list(request):
    page = 'create_list'  # Define the page variable to pass to the template
    if request.method == 'POST':
        form = ToDoListForm(request.POST)
        if form.is_valid():
            to_do_list = form.save(commit=False)
            to_do_list.user = request.user  # Assign the current user as the list owner
            to_do_list.save()
            return redirect('add-items', list_id=to_do_list.id)  # Redirect to the 'add-items' view after creating a list
    else:
        form = ToDoListForm()

    return render(request, 'base/new_list_tasks.html', {'form': form, 'page': page})  # Pass 'page' to the context


@login_required
def add_to_do_item(request, pk):
    page = 'add_items'
    to_do_list = get_object_or_404(ToDoList, id=pk)

    if request.method == 'POST':
        form = ToDoItemForm(request.POST)
        if form.is_valid():
            to_do_item = form.save(commit=False)
            to_do_item.list = to_do_list  # Link the item to the specified list
            to_do_item.save()
            messages.success(request, 'List created successfully')
            return redirect('add-items', pk=to_do_list.id)

    else:
        form = ToDoItemForm()

    context = {
        'form': form,
        'to_do_list': to_do_list,
        'page': page
    }
    return render(request, 'base/new_list_tasks.html', context)


def edit_list_and_items(request, list_id):
    to_do_list = get_object_or_404(ToDoList, id=list_id)

    # Form for editing the list title
    list_form = EditToDoListForm(request.POST or None, instance=to_do_list)

    # Formset for editing items
    ToDoItemFormSet = modelformset_factory(ToDoItem, form=EditToDoItemForm, extra=0)
    item_formset = ToDoItemFormSet(request.POST or None, queryset=to_do_list.items.all())

    if request.method == 'POST':
        if list_form.is_valid() and item_formset.is_valid():
            list_form.save()  # Save the updated list title
            item_formset.save()  # Save all item updates (e.g., description, completed status)
            return redirect('list-details', pk=list_id)  # Redirect to the list details page

    context = {
        'to_do_list': to_do_list,
        'list_form': list_form,
        'item_formset': item_formset,
    }
    print("to_do_list ID:", to_do_list.id)
    return render(request, 'base/edit_list_tasks.html', context)







