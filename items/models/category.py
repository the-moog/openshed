from django.db import models


# Categories.
class Category(models.Model):
    """Category is the collective name for similar products"""
    name = models.CharField(max_length=20, unique=True)

