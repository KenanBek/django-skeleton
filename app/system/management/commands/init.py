import shutil

import os
from django.core import management
from django.core.management.base import NoArgsCommand
from django.conf import settings


class Command(NoArgsCommand):
    help = "Initialize development environment with initial data."

    def ds_print(self, str):
        self.stdout.write('')
        self.stdout.write('>>> DJANGO-SKELETON: ' + str)
        self.stdout.write('')

    def handle_noargs(self, **options):
        base_dir = settings.BASE_DIR

        # DEBUG: Remove current database file
        if settings.DEBUG:
            try:
                self.ds_print('Trying to remove database file...')
                os.remove(settings.DATABASES['default']['NAME'])
                self.ds_print('Database removed')
            except Exception as e:
                self.ds_print('Error on removing database file')
                self.ds_print('ERROR: ' + e.message)

        # DEBUG: Remove static, media and log files
        if settings.DEBUG:
            try:
                self.ds_print('Trying to remove static, media and log files...')
                shutil.rmtree(os.path.join(base_dir, 'files', 'public', 'static'))
                shutil.rmtree(os.path.join(base_dir, 'files', 'public', 'media'))
                os.remove(os.path.join(base_dir, 'files', 'logs', 'django.log'))
                os.remove(os.path.join(base_dir, 'files', 'logs', 'application.log'))
                os.remove(os.path.join(base_dir, 'files', 'logs', 'logic.log'))
            except Exception as e:
                self.ds_print('Error on removing static, media and log files')
                self.ds_print('ERROR: ' + str(e))

        # DEBUG: Remove migration files
        if settings.DEBUG:
            try:
                self.ds_print('Trying to remove migration files...')
                shutil.rmtree(os.path.join(base_dir, 'system', 'migrations'), ignore_errors=True)
                shutil.rmtree(os.path.join(base_dir, 'account', 'migrations'), ignore_errors=True)
                shutil.rmtree(os.path.join(base_dir, 'website', 'migrations'), ignore_errors=True)
                shutil.rmtree(os.path.join(base_dir, 'cart', 'migrations'), ignore_errors=True)
                self.ds_print('Migration files removed')
            except Exception as e:
                self.ds_print('Error on removing migration files')
                self.ds_print('ERROR: ' + str(e))

        # Create (or recreate in case of DEBUG) initial migration files
        try:
            self.ds_print('Trying to create migration scripts...')
            management.call_command('makemigrations', 'system')
            management.call_command('makemigrations', 'account')
            management.call_command('makemigrations', 'website')
            management.call_command('makemigrations', 'cart')
            management.call_command('migrate', interactive=False)
            self.ds_print('Migration scripts created')
        except Exception as e:
            self.ds_print('Error on creating migration scripts')
            self.ds_print('ERROR: ' + str(e))

        # DEBUG: Superuser and Fixtures
        if settings.DEBUG:
            try:
                self.ds_print('Trying to create superuser and load development fixtures...')
                # Superuser
                management.call_command('createsuperuser', username='admin', email='admin@host.local')
                # Fixtures
                management.call_command('loaddata', 'debug_account.json')
                management.call_command('loaddata', 'debug_website.json')
                management.call_command('loaddata', 'debug_cart.json')
                self.ds_print('Superuser created and fixtures loaded')
            except Exception as e:
                self.ds_print('Error on superuser and fixtures creation')
                self.ds_print('ERROR: ' + str(e))


        # DEBUG: Collect static files
        if not settings.DEBUG:
            try:
                self.ds_print('Trying to collect static files...')
                management.call_command('collectstatic', interactive=False)
                self.ds_print('Static files collected')
            except Exception as e:
                self.ds_print('Error on collecting static files')
                self.ds_print('ERROR: ' + str(e))

        # Done
        self.ds_print('Successfully finished.')

