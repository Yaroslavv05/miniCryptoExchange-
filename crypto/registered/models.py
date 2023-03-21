from django.db import models


class KCYModel(models.Model):
    fio = models.CharField(max_length=50)

