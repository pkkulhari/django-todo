from django.shortcuts import render, redirect
from lists.models import Item, TodoList


def home_page(request):
    todoItems = Item.objects.all()

    context = {'todoItems': todoItems}
    return render(request, 'home.html', context)


def new_list(request):
    todoItem = request.POST['todo-item']
    _list = TodoList.objects.create()
    Item.objects.create(body=todoItem, list=_list)
    return redirect('lists:lists', pk=_list.id)


def list_view(request):
    todoItems = Item.objects.all()

    context = {'todoItems': todoItems}
    return render(request, 'list.html', context)


def add_item(request, pk):
    _list = TodoList.objects.get(id=pk)
    todoItem = request.POST['todo-item']
    Item.objects.create(body=todoItem, list=_list)
    return redirect('lists:lists', pk=_list.id)
