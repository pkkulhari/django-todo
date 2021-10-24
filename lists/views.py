from django.shortcuts import render, redirect
from lists.models import Item, TodoList


def home_page(request):

    if request.method == 'POST':
        todoItem = request.POST['todo-item']
        _list = TodoList.objects.create()
        Item.objects.create(body=todoItem, list=_list)
        return redirect('/lists/only-one-list')

    todoItems = Item.objects.all()

    context = {'todoItems': todoItems}
    return render(request, 'home.html', context)


def list_page(request):
    todoItems = Item.objects.all()

    context = {'todoItems': todoItems}
    return render(request, 'home.html', context)
