# django-migration-helper

Django Migration Helper is a simple app containing commands that
make more complicated migrations a lot easier. Use it if you want to
perform some structural changes in your code while keeping the data in your database intact.

## Quick start

1. Run 
```
  pip install django-migration-helper
  
```

2. Add "migration_helper" to your INSTALLED_APPS setting like this::
```
    INSTALLED_APPS = [
        ...
        'migration_helper',
    ]
```
## Basic Usage

**Before using make sure you have applied all your previous migrations! Make sure your 
database state is neutral. Also, as an extra precaution, you may want to dump your database, just in case.
Next, physically move the model between apps and resolve all import dependecies.**
As a next step you run this command:

```
    python manage.py move_model <model_label> <base_app> <target_app> [**options]
```

This command creates migration files for an operation of moving a model (given by `<model_label>`)
from `<base_app>` to `<target_app> `keeping the data already stored
in database intact and resolving all relative fields using
`migrations.SeperateStateAndDatabase` operations.


By default this command only generates migration files. Next step
would be to run `python manage.py migrate`.
If you want to do it automatically, running this command
with `--migrate` flag applies the migrations.
Running this with `--dry-run` doesn't create migration files,
it just shows what operations would be made in the console.

## Credit
Great answer from *Nostalg.io* on stackoverflow [here](http://stackoverflow.com/questions/30601107/move-models-between-django-1-8-apps-with-required-foreignkey-references)


## TODOs
- Provide some unit tests
- Add more commands
