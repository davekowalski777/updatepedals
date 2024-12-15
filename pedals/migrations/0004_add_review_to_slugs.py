from django.db import migrations
from django.utils.text import slugify

def add_review_to_slugs(apps, schema_editor):
    Pedal = apps.get_model('pedals', 'Pedal')
    for pedal in Pedal.objects.all():
        base_slug = f"{pedal.manufacturer.name}-{pedal.name}"
        new_slug = slugify(base_slug) + "-review"
        # Handle potential duplicates by adding a number
        counter = 1
        temp_slug = new_slug
        while Pedal.objects.filter(slug=temp_slug).exclude(id=pedal.id).exists():
            temp_slug = f"{new_slug}-{counter}"
            counter += 1
        pedal.slug = temp_slug
        pedal.save()

def remove_review_from_slugs(apps, schema_editor):
    Pedal = apps.get_model('pedals', 'Pedal')
    for pedal in Pedal.objects.all():
        pedal.slug = slugify(pedal.name)
        pedal.save()

class Migration(migrations.Migration):
    dependencies = [
        ('pedals', '0003_userrating'),
    ]

    operations = [
        migrations.RunPython(add_review_to_slugs, remove_review_from_slugs),
    ]
