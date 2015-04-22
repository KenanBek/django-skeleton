import shutil

import os
from django.core import management
from django.core.management.base import NoArgsCommand
from django.conf import settings


class Command(NoArgsCommand):
    help = "Initialize development environment with initial data."

    def handle_noargs(self, **options):
        base_dir = settings.BASE_DIR

        # DEBUG: Remove current database file
        try:
            os.remove(settings.DATABASES['default']['NAME'])
            self.stdout.write('Database removed')
        except OSError:
            pass

        # DEBUG: Remove media and logs if DEBUG
        if settings.DEBUG:
            try:
                shutil.rmtree(os.path.join(base_dir, 'files', 'public', 'static'), ignore_errors=True)
                shutil.rmtree(os.path.join(base_dir, 'files', 'public', 'media'), ignore_errors=True)
                os.remove(os.path.join(base_dir, 'files', 'logs', 'django.log'))
                os.remove(os.path.join(base_dir, 'files', 'logs', 'application.log'))
                os.remove(os.path.join(base_dir, 'files', 'logs', 'logic.log'))
                self.stdout.write('Public, media and log files removed')
            except Exception as e:
                self.stdout.write('ERROR: ' + str(e))

        # DEBUG: Remove migration files
        if settings.DEBUG:
            try:
                shutil.rmtree(os.path.join(base_dir, 'system', 'migrations'), ignore_errors=True)
                shutil.rmtree(os.path.join(base_dir, 'account', 'migrations'), ignore_errors=True)
                shutil.rmtree(os.path.join(base_dir, 'website', 'migrations'), ignore_errors=True)
                shutil.rmtree(os.path.join(base_dir, 'cart', 'migrations'), ignore_errors=True)
                self.stdout.write('Migration files removed')
            except Exception as e:
                self.stdout.write('ERROR: ' + str(e))

        # Create (or recreate in case of DEBUG) initial migration files
        management.call_command('makemigrations', 'system')
        management.call_command('makemigrations', 'account')
        management.call_command('makemigrations', 'website')
        management.call_command('makemigrations', 'cart')
        management.call_command('migrate', interactive=False)


        # DEBUG: Superuser and Fixtures
        if settings.DEBUG:
            # Superuser
            management.call_command('createsuperuser', username='admin', email='admin@host.local')
            # Fixtures
            management.call_command('loaddata', 'debug_account.json')
            management.call_command('loaddata', 'debug_website.json')
            management.call_command('loaddata', 'debug_cart.json')


        # DEBUG: Collect static
        if not settings.DEBUG:
            management.call_command('collectstatic', interactive=False)

        # Done
        self.stdout.write('Successfully finished.')

