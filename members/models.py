from django.db import models

# Members model.
class Member(models.Model):
    last_name = models.CharField(max_length=20)
    first_name = models.CharField(max_length=20)

    def display_name(self):
        return f"{self.first_name} {self.last_name}"
