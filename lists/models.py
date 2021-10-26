from django.db import models


class TodoList(models.Model):
    pass


class Item(models.Model):
    body = models.TextField()
    list = models.ForeignKey(TodoList, on_delete=models.CASCADE)

    def __str__(self):
        return self.body
