import csv
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from pedals.models import Manufacturer, PedalType, Pedal
from django.db import IntegrityError

class Command(BaseCommand):
    help = 'Import pedals from CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **options):
        csv_file_path = options['csv_file']
        
        with open(csv_file_path, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            
            for row in csv_reader:
                try:
                    # Create or get manufacturer
                    manufacturer, _ = Manufacturer.objects.get_or_create(
                        name=row['Brand'],
                        defaults={
                            'website': '',
                            'about': row.get('About Brand', '')
                        }
                    )

                    # Create or get pedal type
                    pedal_type, _ = PedalType.objects.get_or_create(
                        name=row['Pedal Type'],
                        defaults={
                            'description': f"Collection of {row['Pedal Type']} pedals"
                        }
                    )

                    # Generate base slug
                    base_slug = slugify(f"{row['Brand']}-{row['Pedal Model']}")
                    slug = base_slug
                    counter = 1

                    # Convert rating to decimal if present
                    try:
                        rating = float(row.get('My Rating', 0))
                    except (ValueError, TypeError):
                        rating = None

                    # Keep trying with numbered slugs until we find a unique one
                    while True:
                        try:
                            # Try to create the pedal with current slug
                            pedal = Pedal.objects.create(
                                name=row['Pedal Model'],
                                manufacturer=manufacturer,
                                pedal_type=pedal_type,
                                what_makes_it_good=row.get('What Makes It Good', ''),
                                my_experience=row.get('My Experience', ''),
                                main_features=row.get('Main Features', ''),
                                my_rating=rating,
                                best_for=row.get('Best For', ''),
                                image_url=row.get('Image', ''),
                                affiliate_link=row.get('Affiliate Link', ''),
                                slug=slug
                            )
                            break  # If successful, break the loop
                        except IntegrityError:
                            # If slug exists, try the next number
                            slug = f"{base_slug}-{counter}"
                            counter += 1

                    self.stdout.write(
                        self.style.SUCCESS(f'Successfully imported pedal: {pedal.name}')
                    )
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'Error importing pedal {row["Pedal Model"]}: {str(e)}')
                    )
