from django.db import models


class SecondTestModel(models.Model):
    field = models.CharField(max_length=1)


class TestModel(models.Model):
    test_field = models.CharField(max_length=1)
