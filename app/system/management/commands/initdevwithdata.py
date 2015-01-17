import os

from django.core import management
from django.core.management.base import NoArgsCommand
from django.conf import settings


class Command(NoArgsCommand):
    help = "Initialize development environment settings with initial data for the application."

    def handle_noargs(self, **options):
        # Remove current database file
        try:
            os.remove(settings.DATABASES['default']['NAME'])
            self.stdout.write('Database removed')
        except OSError:
            pass

        # Remove media and logs
        os.system('rm -rf files/public/content')
        os.system('rm -rf files/media/uploads')
        os.system('rm -rf files/logs/*.log')
        self.stdout.write('Public, media and log files removed')

        # Remove migration files
        os.system('rm -rf system/migrations')
        os.system('rm -rf account/migrations')
        os.system('rm -rf website/migrations')
        os.system('rm -rf cart/migrations')
        self.stdout.write('Migration files removed')

        # Migrate
        management.call_command('makemigrations', "system")
        management.call_command('makemigrations', "account")
        management.call_command('makemigrations', "website")
        management.call_command('makemigrations', "cart")
        management.call_command('migrate', interactive=False)

        # Superuser
        management.call_command('createsuperuser', username='admin', email='admin@host.local')

        # Fixtures
        management.call_command('loaddata', "dev_account")
        management.call_command('loaddata', "dev_website")
        management.call_command('loaddata', "dev_cart")

        # Collect static
        if not settings.DEBUG:
            management.call_command('collectstatic', interactive=False)

        # Done
        self.stdout.write('Successfully finished.')

