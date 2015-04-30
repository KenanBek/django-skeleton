from django.conf import settings
from django.core import management


class CommandHelper:
    def __init__(self, command):
        self.base_dir = settings.BASE_DIR
        self.command = command
        self.string_queue = []

    def add_to_print_queue(self, s):
        self.string_queue.append(s)

    def print_queue(self):
        self.command.stdout.write('')
        self.command.stdout.write('>>> DJANGO-SKELETON:')
        for item in self.string_queue:
            self.command.stdout.write(str(item))
        self.command.stdout.write('')

    def load_fixtures(self):
        management.call_command('loaddata', 'debug_account.json')
        management.call_command('loaddata', 'debug_blog.json')
        management.call_command('loaddata', 'debug_cart.json')

