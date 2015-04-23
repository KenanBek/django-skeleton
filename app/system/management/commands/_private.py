import shutil
from django.conf import settings

import os
from django.core import management


class CommandHelper:
    def __init__(self, command):
        self.base_dir = settings.BASE_DIR
        self.command = command

    def ds_print(self, str):
        self.command.stdout.write('')
        self.command.stdout.write('>>> DJANGO-SKELETON: ' + str)
        self.command.stdout.write('')

    def remove_migrations(self):
        shutil.rmtree(os.path.join(self.command.base_dir, 'system', 'migrations'))
        shutil.rmtree(os.path.join(self.command.base_dir, 'account', 'migrations'))
        shutil.rmtree(os.path.join(self.command.base_dir, 'website', 'migrations'))
        shutil.rmtree(os.path.join(self.command.base_dir, 'cart', 'migrations'))

    def makemigrations_and_migrate(self):
        management.call_command('makemigrations', 'system')
        management.call_command('makemigrations', 'account')
        management.call_command('makemigrations', 'website')
        management.call_command('makemigrations', 'cart')
        management.call_command('migrate', interactive=False)

    def load_fixtures(self):
        management.call_command('loaddata', 'debug_account.json')
        management.call_command('loaddata', 'debug_website.json')
        management.call_command('loaddata', 'debug_cart.json')

