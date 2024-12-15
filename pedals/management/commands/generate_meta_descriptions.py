from django.core.management.base import BaseCommand
from pedals.models import Pedal
import random

class Command(BaseCommand):
    help = 'Generate unique meta descriptions for pedals'

    def generate_pedal_meta(self, pedal):
        # Base templates for meta descriptions
        templates = [
            "{brand} {model} review: {type} pedal with {feature}. {rating_text}",
            "Discover the {brand} {model}, a {type} pedal that {benefit}. {rating_text}",
            "Expert review of {brand} {model}: {type} pedal {feature}. {rating_text}",
            "{brand} {model} {type} pedal: {benefit}. {rating_text}",
            "Looking for a {type} pedal? {brand} {model} review: {feature}. {rating_text}"
        ]

        # Feature templates based on pedal type
        feature_templates = {
            'Delay': [
                "crystal-clear repeats",
                "warm analog echoes",
                "versatile delay options",
                "pristine digital delays"
            ],
            'Reverb': [
                "lush ambient sounds",
                "studio-quality reverb",
                "spacious atmosphere",
                "rich room emulation"
            ],
            'Overdrive': [
                "smooth drive tones",
                "transparent overdrive",
                "tube-like warmth",
                "dynamic response"
            ],
            'Distortion': [
                "high-gain tones",
                "aggressive distortion",
                "metal-ready sound",
                "thick saturation"
            ],
            'Modulation': [
                "swirling modulation",
                "classic chorus sounds",
                "vibrant phase shifts",
                "expressive modulation"
            ],
            'Compression': [
                "dynamic control",
                "smooth compression",
                "punchy attack",
                "balanced sustain"
            ]
        }

        # Benefit templates
        benefit_templates = [
            "delivers professional sound quality",
            "offers exceptional tone shaping",
            "brings versatility to your board",
            "elevates your guitar tone",
            "provides outstanding performance"
        ]

        # Generate rating text
        rating_text = ""
        if pedal.my_rating:
            rating_text = f"Rated {pedal.my_rating}/5"

        # Get features for this pedal type
        pedal_type = pedal.pedal_type.name if pedal.pedal_type else "Effect"
        features = feature_templates.get(pedal_type, ["premium sound quality", "versatile controls", "professional features"])

        # Fill in the template
        template = random.choice(templates)
        meta = template.format(
            brand=pedal.manufacturer.name,
            model=pedal.name,
            type=pedal_type.lower(),
            feature=random.choice(features),
            benefit=random.choice(benefit_templates),
            rating_text=rating_text
        )

        # Ensure it's not too long
        if len(meta) > 155:
            meta = meta[:152] + "..."

        return meta

    def handle(self, *args, **options):
        pedals = Pedal.objects.all()
        used_descriptions = set()

        for pedal in pedals:
            # Keep generating until we get a unique description
            while True:
                meta = self.generate_pedal_meta(pedal)
                if meta not in used_descriptions:
                    used_descriptions.add(meta)
                    pedal.meta_description = meta
                    pedal.save()
                    self.stdout.write(self.style.SUCCESS(f'Generated meta for {pedal.name}: {meta}'))
                    break

        self.stdout.write(self.style.SUCCESS('Successfully generated meta descriptions'))
