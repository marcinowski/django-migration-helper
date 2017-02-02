from django.db import models


class SimpleBaseOne(models.Model):
    test_field = models.CharField(max_length=4, default='test_base_one')


class SimpleBaseTwo(models.Model):
    test_field = models.CharField(max_length=4, default='test_base_two')


class SimpleBaseThree(models.Model):
    test_field = models.CharField(max_length=4, default='test_base_three')


class SimpleBaseFour(models.Model):
    test_field = models.CharField(max_length=4, default='test_base_four')


class SimpleBaseMeta(models.Model):
    test_field = models.CharField(max_length=4, default='test_base_meta')

    class Meta:
        db_table = 'test_base_meta'


class RelationalBaseModel(models.Model):
    test_fk = models.ForeignKey('foreign_app.SimpleForeignOne')
    test_o2o = models.OneToOneField('foreign_app.SimpleForeignTwo')
    test_m2m = models.ManyToManyField('foreign_app.SimpleForeignThree')
    test_m2m_db_table = models.ManyToManyField('foreign_app.SimpleForeignFour', db_table='test_base_relational')
    test_m2m_through = models.ManyToManyField(
        'foreign_app.SimpleForeignFive', through='foreign_app.SimpleForeignThrough')


class RelationalBaseModelMeta(models.Model):
    test_fk = models.ForeignKey('foreign_app.SimpleForeignOne')
    test_o2o = models.OneToOneField('foreign_app.SimpleForeignTwo')
    test_m2m = models.ManyToManyField('foreign_app.SimpleForeignThree')
    test_m2m_db_table = models.ManyToManyField('foreign_app.SimpleForeignFour', db_table='test_mm_base_relational_meta')
    test_m2m_through = models.ManyToManyField(
        'foreign_app.SimpleForeignFive', through='foreign_app.SimpleForeignThroughMeta')

    class Meta:
        db_table = 'test_base_relational_meta'


class SimpleBaseThrough(models.Model):
    test_field_base = models.ForeignKey(SimpleBaseThree)
    test_field_foreign = models.ForeignKey('foreign_app.RelationalForeignModel')


class SimpleBaseThroughMeta(models.Model):
    test_field_base = models.ForeignKey(SimpleBaseThree)
    test_field_foreign = models.ForeignKey('foreign_app.RelationalForeignModelMeta')
