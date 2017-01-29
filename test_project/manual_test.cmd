pip uninstall django-migration-helper -y
python %~dp0..\django-migration-helper\setup.py sdist
pip install %~dp0..\django-migration-helper
python %~dp0manage.py move_model testmodel base_app target_app