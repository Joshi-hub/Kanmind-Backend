from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Erstellt den Gast-User für den Guest-Login im Frontend'

    def handle(self, *args, **options):
        email = 'kevin@kovacsi.de'
        password = 'asdasdasd'
        first_name = 'Guest'
        last_name = 'User'

        if User.objects.filter(email=email).exists():
            self.stdout.write(self.style.WARNING(f'Gast-User "{email}" existiert bereits.'))
            return

        User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        self.stdout.write(self.style.SUCCESS(f'Gast-User "{email}" wurde erfolgreich erstellt.'))
