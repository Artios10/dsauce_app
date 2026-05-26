import os

from django.core.management.base import BaseCommand, CommandError

from apps.authentication.models import User, UserRole


class Command(BaseCommand):
    help = 'Seed the initial admin user from environment variables.'

    def handle(self, *args, **options):
        email = os.environ.get('ADMIN_SEED_EMAIL')
        username = os.environ.get('ADMIN_SEED_USERNAME')
        password = os.environ.get('ADMIN_SEED_PASSWORD')

        if not email or not username or not password:
            raise CommandError('ADMIN_SEED_EMAIL, ADMIN_SEED_USERNAME, and ADMIN_SEED_PASSWORD are required.')

        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                'username': username,
                'role': UserRole.ADMIN,
                'is_staff': True,
                'is_superuser': True,
                'is_verified': True,
                'is_active': True,
            },
        )
        user.username = username
        user.role = UserRole.ADMIN
        user.is_staff = True
        user.is_superuser = True
        user.is_verified = True
        user.is_active = True
        user.set_password(password)
        user.save()

        if created:
            self.stdout.write(self.style.SUCCESS('Admin user created successfully.'))
        else:
            self.stdout.write(self.style.SUCCESS('Admin user updated successfully.'))
