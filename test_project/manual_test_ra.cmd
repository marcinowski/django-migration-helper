del /Q %~dp0db.sqlite3
pip uninstall django-migration-helper -y
python %~dp0..\django-migration-helper\setup.py sdist
pip install %~dp0..\django-migration-helper
python %~dp0manage.py migrate
python %~dp0manage.py rename_app rename_app rename_app_test