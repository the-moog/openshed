from django.db import models


# Members model.
class Member(models.Model):
    last_name = models.CharField(max_length=20)
    first_name = models.CharField(max_length=20)
    username = models.CharField(max_length=20)
    departure_date = models.DateField(null=True)

    def display_name(self):
        return f"{self.first_name} {self.last_name}"
