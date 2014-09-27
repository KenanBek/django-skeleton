import os

from django.core import management
from django.core.management.base import NoArgsCommand
from django.conf import settings


class Command(NoArgsCommand):
    help = 'Syncdb and create admin user'

    def handle_noargs(self, **options):
        try:
            os.remove(settings.DATABASES['default']['NAME'])
        except OSError:
            pass
        management.call_command('syncdb', interactive=False)
        management.call_command('createsuperuser')
        self.stdout.write('Successfully initialized.')

