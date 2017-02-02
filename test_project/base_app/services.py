from django.apps import apps

from base_app import models as base
from foreign_app import models as foreign


class FillDatabase(object):
    @classmethod
    def run(cls, clean_db=True):
        cls._clear_database() if clean_db else None
        cls._fill_simple_models()
        cls._resolve_base_relational_models()
        cls._resolve_foreign_relational_models()
        cls._resolve_m2m_through_models()

    @staticmethod
    def _clear_database():
        for app_label in ('base_app', 'foreign_app'):
            for model in apps.get_app_config(app_label).models.values():
                model.objects.all().delete()

    @staticmethod
    def _fill_simple_models():
        base.SimpleBaseOne.objects.create()
        base.SimpleBaseTwo.objects.create()
        base.SimpleBaseThree.objects.create()
        base.SimpleBaseFour.objects.create()
        foreign.SimpleForeignOne.objects.create()
        foreign.SimpleForeignTwo.objects.create()
        foreign.SimpleForeignThree.objects.create()
        foreign.SimpleForeignFour.objects.create()
        foreign.SimpleForeignFive.objects.create()

    @staticmethod
    def _resolve_base_relational_models():
        model = base.RelationalBaseModel.objects.create(
            test_fk=foreign.SimpleForeignOne.objects.get(),
            test_o2o=foreign.SimpleForeignTwo.objects.get(),
        )
        model.test_m2m.add(foreign.SimpleForeignThree.objects.get())
        model.test_m2m_db_table.add(foreign.SimpleForeignFour.objects.get())

        model = base.RelationalBaseModelMeta.objects.create(
            test_fk=foreign.SimpleForeignOne.objects.get(),
            test_o2o=foreign.SimpleForeignTwo.objects.get(),
        )
        model.test_m2m.add(foreign.SimpleForeignThree.objects.get())
        model.test_m2m_db_table.add(foreign.SimpleForeignFour.objects.get())

    @staticmethod
    def _resolve_foreign_relational_models():
        model = foreign.RelationalForeignModel.objects.create()
        model.test_field_m2m.add(base.SimpleBaseTwo.objects.get())
        model.test_field_m2m.add(base.SimpleBaseTwo.objects.get())

        model = foreign.RelationalForeignModelMeta.objects.create()
        model.test_field_m2m.add(base.SimpleBaseTwo.objects.get())
        model.test_field_m2m.add(base.SimpleBaseTwo.objects.get())

    @staticmethod
    def _resolve_m2m_through_models():
        base.SimpleBaseThrough.objects.create(
            test_field_base=base.SimpleBaseThree.objects.get(),
            test_field_foreign=foreign.RelationalForeignModel.objects.get(),
        )
        base.SimpleBaseThroughMeta.objects.create(
            test_field_base=base.SimpleBaseThree.objects.get(),
            test_field_foreign=foreign.RelationalForeignModelMeta.objects.get(),
        )
        foreign.SimpleForeignThrough.objects.create(
            test_field_foreign=foreign.SimpleForeignFive.objects.get(),
            test_field_base=base.RelationalBaseModel.objects.get(),
        )
        foreign.SimpleForeignThroughMeta.objects.create(
            test_field_foreign=foreign.SimpleForeignFive.objects.get(),
            test_field_base=base.RelationalBaseModelMeta.objects.get(),
        )
