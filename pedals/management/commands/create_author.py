from django.core.management.base import BaseCommand
from pedals.models import Author

class Command(BaseCommand):
    help = 'Creates the default author profile for Dave'

    def handle(self, *args, **kwargs):
        author, created = Author.objects.get_or_create(
            name='Dave',
            defaults={
                'bio': 'Hi! I\'m Dave, a passionate guitarist with 15 years of experience playing various styles of music. I\'ve tested and owned countless guitar pedals over the years, and I love sharing my insights to help other guitarists find their perfect tone.',
                'years_of_experience': 15,
                'profile_image': None  # You can add a profile image URL later if desired
            }
        )

        if created:
            self.stdout.write(self.style.SUCCESS('Successfully created author profile for Dave'))
        else:
            self.stdout.write(self.style.SUCCESS('Author profile for Dave already exists'))
