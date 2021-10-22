from django.db import models


class Item(models.Model):
    body = models.TextField()
