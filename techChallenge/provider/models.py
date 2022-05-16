from django.db import models

# Create your models here.
class Provider(models.Model):
    name = models.CharField(max_length=128, null=False)
    email = models.CharField(max_length=128, unique=True, null=False)
    phone_number = models.CharField(max_length=15, unique=True, null=False)
    language = models.CharField(max_length=30)
    currency = models.CharField(max_length=30)

    def __str__(self):
        return f"Provider({self.name!r}, {self.email!r}, {self.phone_number!r}, {self.language!r}, {self.currency!r})"