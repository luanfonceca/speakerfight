from django.core import management

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = """
        Deploy commands calls the following django commands:
        ['check', 'clean_pyc', 'migrate', 'compilemessages']
    """
    commands = [
        'check', 'clean_pyc',
        'migrate', 'compilemessages'
    ]

    def handle(self, *args, **kwargs):
        for command in self.commands:
            management.call_command(command, interactive=False)
