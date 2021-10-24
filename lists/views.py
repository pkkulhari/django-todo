from django.shortcuts import render, redirect
from lists.models import Item


def home_page(request):

    if request.method == 'POST':
        todoItem = request.POST['todo-item']
        Item.objects.create(body=todoItem)
        return redirect('lists:home')

    todoItems = Item.objects.all()

    context = {'todoItems': todoItems}
    return render(request, 'home.html', context)
