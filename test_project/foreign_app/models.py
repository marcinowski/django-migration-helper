from django.db import models

from base_app import models as base


class SimpleForeignOne(models.Model):
    test_field = models.CharField(max_length=4, default='test_foreign_one')


class SimpleForeignTwo(models.Model):
    test_field = models.CharField(max_length=4, default='test_foreign_two')


class SimpleForeignThree(models.Model):
    test_field = models.CharField(max_length=4, default='test_foreign_three')


class SimpleForeignFour(models.Model):
    test_field = models.CharField(max_length=4, default='test_foreign_four')


class SimpleForeignFive(models.Model):
    test_field = models.CharField(max_length=4, default='test_foreign_five')


class RelationalForeignModel(models.Model):
    test_field_m2m = models.ManyToManyField(base.SimpleBaseTwo)
    test_field_m2m_through = models.ManyToManyField(base.SimpleBaseThree, through=base.SimpleBaseThrough)
    test_field_m2m_db_table = models.ManyToManyField(base.SimpleBaseFour, db_table='test_foreign_relational')


class RelationalForeignModelMeta(models.Model):
    test_field_m2m = models.ManyToManyField(base.SimpleBaseTwo)
    test_field_m2m_through = models.ManyToManyField(base.SimpleBaseThree, through=base.SimpleBaseThroughMeta)
    test_field_m2m_db_table = models.ManyToManyField(base.SimpleBaseFour, db_table='test_mm_foreign_relational_meta')

    class Meta:
        db_table = 'test_foreign_relational_meta'


class SimpleForeignThrough(models.Model):
    test_field_foreign = models.ForeignKey(SimpleForeignFive)
    test_field_base = models.ForeignKey(base.RelationalBaseModel)


class SimpleForeignThroughMeta(models.Model):
    test_field_foreign = models.ForeignKey(SimpleForeignFive)
    test_field_base = models.ForeignKey(base.RelationalBaseModelMeta)
