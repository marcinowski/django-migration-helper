from django.db import models

from base_app.models import TestModel
from target_app.models import SecondTestModel


class TestFKModel(models.Model):
    test_fk = models.ForeignKey(TestModel)
    test_second_fk = models.ForeignKey(SecondTestModel)


class TestM2MModel(models.Model):
    test_m2m = models.ManyToManyField(TestModel)
    test_second_m2m = models.ManyToManyField(SecondTestModel)


class TestO2OModel(models.Model):
    test_o2o = models.OneToOneField(TestModel)
    test_second_o2o = models.OneToOneField(SecondTestModel)
