# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-02 00:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('base_app', '0001_initial'),
        ('foreign_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='simplebasethroughmeta',
            name='test_field_foreign',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='foreign_app.RelationalForeignModelMeta'),
        ),
        migrations.AddField(
            model_name='simplebasethrough',
            name='test_field_base',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base_app.SimpleBaseThree'),
        ),
        migrations.AddField(
            model_name='simplebasethrough',
            name='test_field_foreign',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='foreign_app.RelationalForeignModel'),
        ),
        migrations.AddField(
            model_name='relationalbasemodelmeta',
            name='test_fk',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='foreign_app.SimpleForeignOne'),
        ),
        migrations.AddField(
            model_name='relationalbasemodelmeta',
            name='test_m2m',
            field=models.ManyToManyField(to='foreign_app.SimpleForeignThree'),
        ),
        migrations.AddField(
            model_name='relationalbasemodelmeta',
            name='test_m2m_db_table',
            field=models.ManyToManyField(db_table='test_mm_base_relational_meta', to='foreign_app.SimpleForeignFour'),
        ),
        migrations.AddField(
            model_name='relationalbasemodelmeta',
            name='test_m2m_through',
            field=models.ManyToManyField(through='foreign_app.SimpleForeignThroughMeta', to='foreign_app.SimpleForeignFive'),
        ),
        migrations.AddField(
            model_name='relationalbasemodelmeta',
            name='test_o2o',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='foreign_app.SimpleForeignTwo'),
        ),
        migrations.AddField(
            model_name='relationalbasemodel',
            name='test_fk',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='foreign_app.SimpleForeignOne'),
        ),
        migrations.AddField(
            model_name='relationalbasemodel',
            name='test_m2m',
            field=models.ManyToManyField(to='foreign_app.SimpleForeignThree'),
        ),
        migrations.AddField(
            model_name='relationalbasemodel',
            name='test_m2m_db_table',
            field=models.ManyToManyField(db_table='test_base_relational', to='foreign_app.SimpleForeignFour'),
        ),
        migrations.AddField(
            model_name='relationalbasemodel',
            name='test_m2m_through',
            field=models.ManyToManyField(through='foreign_app.SimpleForeignThrough', to='foreign_app.SimpleForeignFive'),
        ),
        migrations.AddField(
            model_name='relationalbasemodel',
            name='test_o2o',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='foreign_app.SimpleForeignTwo'),
        ),
    ]
