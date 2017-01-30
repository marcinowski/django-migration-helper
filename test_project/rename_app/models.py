from django.db import models


class TestModelRenamedApp(models.Model):
    text = models.CharField(max_length=1)


class TestSecondModelRenamedApp(models.Model):
    test_m2m = models.ManyToManyField('foreign_app.TestRenamedModel')
