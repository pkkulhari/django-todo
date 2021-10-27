from django.urls import path

from lists import views

app_name = 'lists'
urlpatterns = [
    path('', views.home_page, name='home'),
    path('lists/<int:pk>/', views.list_view, name='lists'),
    path('lists/new/', views.new_list, name='new-list'),
    path('lists/<int:pk>/add/', views.add_item, name='add-item'),
]
