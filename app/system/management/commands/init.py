import shutil

import os
from django.core import management
from django.core.management.base import NoArgsCommand
from django.conf import settings
from system.management.commands._private import CommandHelper


class Command(NoArgsCommand):
    help = "Initialize application's environment."

    def __init__(self):
        super(Command, self).__init__()
        self.base_dir = settings.BASE_DIR
        self.helper = CommandHelper(self)

    def handle_noargs(self, **options):
        # DEBUG: Remove current database file
        if settings.DEBUG:
            try:
                self.helper.ds_print('Trying to remove database file...')
                os.remove(settings.DATABASES['default']['NAME'])
                self.helper.ds_print('Database removed')
            except Exception as e:
                self.helper.ds_print('Error on removing database file')
                self.helper.ds_print('ERROR: ' + e.message)

        # DEBUG: Remove static, media and log files
        if settings.DEBUG:
            try:
                self.helper.ds_print('Trying to remove static, media and log files...')
                shutil.rmtree(os.path.join(self.base_dir, 'files', 'public', 'static'))
                shutil.rmtree(os.path.join(self.base_dir, 'files', 'public', 'media'))
                os.remove(os.path.join(self.base_dir, 'files', 'logs', 'django.log'))
                os.remove(os.path.join(self.base_dir, 'files', 'logs', 'application.log'))
                os.remove(os.path.join(self.base_dir, 'files', 'logs', 'logic.log'))
            except Exception as e:
                self.helper.ds_print('Error on removing static, media and log files')
                self.helper.ds_print('ERROR: ' + str(e))

        # DEBUG: Remove migration files
        if settings.DEBUG:
            try:
                self.helper.ds_print('Trying to remove migration files...')
                self.helper.remove_migrations()
                self.helper.ds_print('Migration files removed')
            except Exception as e:
                self.helper.ds_print('Error on removing migration files')
                self.helper.ds_print('ERROR: ' + str(e))

        # Create (or recreate in case of DEBUG) initial migration files
        try:
            self.helper.ds_print('Trying to create migration scripts and migrate...')
            self.helper.makemigrations_and_migrate()
            self.helper.ds_print('Migration scripts created')
        except Exception as e:
            self.helper.ds_print('Error on creating migration scripts and migrate')
            self.helper.ds_print('ERROR: ' + str(e))

        # DEBUG: Superuser and Fixtures
        if settings.DEBUG:
            try:
                self.helper.ds_print('Trying to create superuser and load development fixtures...')
                # Superuser
                management.call_command('createsuperuser', username='admin', email='admin@host.local')
                # Fixtures
                self.helper.load_fixtures()
                self.helper.ds_print('Superuser created and fixtures loaded')
            except Exception as e:
                self.helper.ds_print('Error on superuser and fixtures creation')
                self.helper.ds_print('ERROR: ' + str(e))


        # NOT DEBUG: Collect static files
        if not settings.DEBUG:
            try:
                self.helper.ds_print('Trying to collect static files...')
                management.call_command('collectstatic', interactive=False)
                self.helper.ds_print('Static files collected')
            except Exception as e:
                self.helper.ds_print('Error on collecting static files')
                self.helper.ds_print('ERROR: ' + str(e))

        # Done
        self.helper.ds_print('Successfully finished.')

