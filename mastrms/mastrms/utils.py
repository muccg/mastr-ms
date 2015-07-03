from dingus import patch

__all__ = ["migration_loaddata"]


def migration_loaddata(orm, fixture_name):
    """
    Use this function for loading bulk data in migrations.
    See: http://south.aeracode.org/ticket/334
         http://stackoverflow.com/a/5906258
    """
    _get_model = lambda model_identifier: orm[model_identifier]

    with patch('django.core.serializers.python._get_model', _get_model):
        from django.core.management import call_command
        call_command("loaddata", fixture_name)
