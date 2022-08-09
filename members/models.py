from django.db import models
from django.contrib.auth.models import AbstractUser


# Members model.
class Member(AbstractUser):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    departure_date = models.DateField(null=True)

    def display_name(self):
        return f"{self.first_name} {self.last_name} ({self.username})"

    def __str__(self):
        return self.display_name()


