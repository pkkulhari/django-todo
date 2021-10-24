from django.db import models


class Item(models.Model):
    body = models.TextField()

    def __str__(self):
        return self.body
