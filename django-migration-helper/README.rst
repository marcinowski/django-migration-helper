=======================
Django Migration Helper
=======================

Django Migration Helper is a simple app containing commands that
make more complicated migrations a lot easier.

Quick start
-----------

1. Add "migration_helper" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'migration_helper',
    ]

Basic Usage
-----------
Before using make sure you have applied all your migrations!
Next, move the model and resolve all import dependecies.
::
    move_model <model_label> <base_app> <target_app> [options]

This command creates migration files (given by <model_label>)
from <base_app> to <target_app> keeping the data already stored
in database intact and resolving all relative models using
SeperateStateAndDatabase operations.
Before running this command you must physically move the model
between apps and resolve all import dependencies.
By default this command generates only migration files. Next step
would be to run "python manage.py migrate".
If you want to do it automatically, running this command
with --migrate flag executes the migrations.
Running this with --dry-run doesn't create migration files,
it just shows what operations would be made in the console.
