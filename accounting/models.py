from django.db import models


class Account(models.Model):
    name = models.CharField(max_length=80)

    def __str__(self):
        return self.name


class Klass(models.Model):
    name = models.CharField(max_length=80)

    def __str__(self):
        return self.name
