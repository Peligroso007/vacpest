from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Creating Table, could take upto 5 min'))
        call_command('migrate')
        self.stdout.write(self.style.SUCCESS('Table created successfully'))
        self.stdout.write(self.style.SUCCESS('Running Fixture'))
        call_command('loaddata', 'app/fixtures/User.json')
        self.stdout.write(self.style.SUCCESS('Data added successfully'))
