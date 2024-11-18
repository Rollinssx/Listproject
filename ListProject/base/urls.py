from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('list_details/<int:pk>/', views.list_detail, name='list-details'),
    path('update_item/<str:pk>/', views.update_item, name='update_item'),
    path('list_view/', views.list_view, name='list-view'),
    path('create_list/', views.create_to_do_list, name='create-list'),
    path('add_items/<int:pk>/', views.add_to_do_item, name='add-items'),
    path('edit_list/<int:list_id>/', views.edit_list_and_items, name='edit-list'),

    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_page, name='logout'),
    path('register/', views.register_page, name='register'),
]


