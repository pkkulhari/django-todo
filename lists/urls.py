from django.urls import path

from lists import views

app_name = 'lists'
urlpatterns = [
    path('<int:pk>/', views.list_view, name='lists'),
    path('new/', views.new_list, name='new-list'),
    path('<int:pk>/add/', views.add_item, name='add-item'),
]
