from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from provider.models import Provider


class Polygon(models.Model):
    p_name = models.CharField(max_length=100)
    price = models.FloatField()
    information = models.PolygonField()
    name = models.ForeignKey(Provider, to_field="name",
                             db_column="name", on_delete=models.CASCADE)

    def __str__(self):
        return f"\n- Polygon({self.p_name!r}, {self.price!r}, {self.information!r})"
