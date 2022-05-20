from django.db import models
# Create your models here.


class Provider(models.Model):
    name = models.CharField(max_length=128, unique=True, null=False)
    email = models.CharField(max_length=128, null=False)
    phone_number = models.CharField(max_length=15, null=True)
    language = models.CharField(max_length=30, null=True)
    currency = models.CharField(max_length=30, null=True)

    def __str__(self):
        return f"\n- Provider({self.name!r}, {self.email!r}, {self.phone_number!r}, \
                {self.language!r}, {self.currency!r})"
