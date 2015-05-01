import shutil
import os

from django.core import management
from django.core.management.base import NoArgsCommand
from django.conf import settings

from ._private import CommandHelper


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
                self.helper.add_to_print_queue('Trying to remove database file...')
                os.remove(settings.DATABASES['default']['NAME'])
                self.helper.add_to_print_queue('Database removed')
            except Exception as e:
                self.helper.add_to_print_queue('Error on removing database file')
                self.helper.add_to_print_queue('ERROR: ' + e.message)

        # DEBUG: Remove static, media and log files
        if settings.DEBUG:
            try:
                self.helper.add_to_print_queue('Trying to remove static, media and log files...')
                shutil.rmtree(os.path.join(self.base_dir, 'files', 'public', 'media'))
                os.remove(os.path.join(self.base_dir, 'files', 'logs', 'django.log'))
                os.remove(os.path.join(self.base_dir, 'files', 'logs', 'application.log'))
                os.remove(os.path.join(self.base_dir, 'files', 'logs', 'logic.log'))
                shutil.rmtree(os.path.join(self.base_dir, 'files', 'public', 'static'))
            except Exception as e:
                self.helper.add_to_print_queue('Error on removing static, media and log files')
                self.helper.add_to_print_queue('ERROR: ' + str(e))

        # DEBUG: Migrate, Superuser and Fixtures
        if settings.DEBUG:
            try:
                self.helper.add_to_print_queue('Trying to migrate, create superuser and load development fixtures...')
                # Migrate
                management.call_command('migrate', interactive=False)
                # Superuser
                management.call_command('createsuperuser', username='admin', email='admin@host.local')
                # Fixtures
                self.helper.load_fixtures()
                self.helper.add_to_print_queue('Migrated, superuser created and fixtures loaded')
            except Exception as e:
                self.helper.add_to_print_queue('Error on migrate, superuser and fixtures creation')
                self.helper.add_to_print_queue('ERROR: ' + str(e))

        # NOT DEBUG: Collect static files
        if not settings.DEBUG:
            try:
                self.helper.add_to_print_queue('Trying to collect static files...')
                management.call_command('collectstatic', interactive=False)
                self.helper.add_to_print_queue('Static files collected')
            except Exception as e:
                self.helper.add_to_print_queue('Error on collecting static files')
                self.helper.add_to_print_queue('ERROR: ' + str(e))

        # Done
        self.helper.add_to_print_queue('Successfully finished.')
        self.helper.print_queue()

