from django.contrib.gis.db import models
from provider.models import Provider


class Polygon(models.Model):
    p_name = models.CharField(max_length=100)
    price = models.FloatField()
    information = models.PolygonField()
    provider = models.ForeignKey(Provider, to_field="name",
                                 db_column="name", on_delete=models.CASCADE)

    def __str__(self):
        return f"\n- N° {self.id}: name = {self.p_name!r}, \
                provider_name = {self.provider.name!r}, price = {self.price!r}"
