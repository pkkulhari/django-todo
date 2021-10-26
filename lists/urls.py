from django.urls import path

from lists import views

app_name = 'lists'
urlpatterns = [
    path('', views.home_page, name='home'),
    path('lists/new/', views.new_list, name='new-list'),
]
