from django.conf import settings
from django.core import management
from django.core.management.base import NoArgsCommand

from ._private import CommandHelper


class Command(NoArgsCommand):
    help = "Check application's environment."

    def __init__(self):
        super(Command, self).__init__()
        self.base_dir = settings.BASE_DIR
        self.helper = CommandHelper(self)

    def handle_noargs(self, **options):
        # NOT DEBUG: Collect static files
        if not settings.DEBUG:
            management.call_command('collectstatic', interactive=False)

        # Done
        self.helper.add_to_print_queue('Successfully finished.')
        self.helper.print_queue()

