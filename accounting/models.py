from django.db import models


class Account(models.Model):
    name = models.CharField(max_length=80)

    def __str__(self):
        return self.name


class Klass(models.Model):
    name = models.CharField(max_length=80)

    class Meta(object):
        verbose_name = 'Class'
        verbose_name_plural = 'Classes'

    def __str__(self):
        return self.name
