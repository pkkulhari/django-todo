from django.shortcuts import render, redirect
from lists.models import Item, TodoList


def home_page(request):

    if request.method == 'POST':
        todoItem = request.POST['todo-item']
        _list = TodoList.objects.create()
        Item.objects.create(body=todoItem, list=_list)
        return redirect('lists:lists')

    todoItems = Item.objects.all()

    context = {'todoItems': todoItems}
    return render(request, 'home.html', context)
