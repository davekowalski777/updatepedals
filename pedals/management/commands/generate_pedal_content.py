from django.core.management.base import BaseCommand
from pedals.models import Pedal
import random

class Command(BaseCommand):
    help = 'Generates unique, engaging content for pedals while preserving original features and genres'

    def get_tone_description(self, pedal_type, pedal_name):
        distortion_words = [
            "crushing", "thick", "saturated", "aggressive", "warm", "rich", "harmonically rich",
            "tight", "responsive", "dynamic", "smooth", "creamy", "compressed", "gritty", "raw",
            "fierce", "punchy", "fat", "woolly", "sizzling", "molten", "crunchy", "biting"
        ]
        delay_words = [
            "pristine", "warm", "analog-like", "crystal clear", "dark", "ambient", "spacious",
            "wide", "three-dimensional", "immersive", "atmospheric", "ethereal", "haunting",
            "tape-like", "lo-fi", "pristine", "shimmering", "cascading", "hypnotic"
        ]
        reverb_words = [
            "lush", "spacious", "ethereal", "ambient", "dreamy", "expansive", "natural",
            "room-filling", "shimmering", "heavenly", "cavernous", "infinite", "ghostly",
            "angelic", "cathedral-like", "plate-like", "spring-like", "cosmic"
        ]
        modulation_words = [
            "swirling", "liquid", "organic", "pulsating", "hypnotic", "subtle", "deep",
            "rich", "dimensional", "evolving", "dynamic", "watery", "psychedelic", "swooshing",
            "undulating", "throbbing", "spinning", "warbling"
        ]

        type_lower = pedal_type.name.lower()
        word_list = []
        
        if "distortion" in type_lower or "overdrive" in type_lower or "fuzz" in type_lower:
            word_list = distortion_words
        elif "delay" in type_lower:
            word_list = delay_words
        elif "reverb" in type_lower:
            word_list = reverb_words
        elif "modulation" in type_lower or "chorus" in type_lower or "phaser" in type_lower:
            word_list = modulation_words
        else:
            word_list = distortion_words + delay_words + reverb_words + modulation_words

        # Add some randomness to the selection process
        if random.random() < 0.3:  # 30% chance to mix in words from other categories
            other_words = random.choice([distortion_words, delay_words, reverb_words, modulation_words])
            word_list.extend(other_words[:5])

        return random.sample(word_list, 3)

    def generate_what_makes_it_good(self, pedal):
        tone_words = self.get_tone_description(pedal.pedal_type, pedal.name)
        
        templates = [
            f"The {pedal.name} is a game-changer in the world of {pedal.pedal_type.name.lower()} pedals. It's got this {tone_words[0]} character that just oozes personality, while still maintaining a {tone_words[1]} foundation that works in any mix. What really sets it apart is how {tone_words[2]} it can get - perfect for creating your own signature sound.",
            
            f"Look, I've played through countless pedals, but the {pedal.name} hits different. First off, you've got this incredibly {tone_words[0]} response that feels alive under your fingers. Then there's the {tone_words[1]} quality that just makes everything sound better. But the real magic? That {tone_words[2]} sweet spot that makes you lose track of time while playing.",
            
            f"There's something special about how the {pedal.name} approaches {pedal.pedal_type.name.lower()}. Instead of trying to do everything, it focuses on delivering a {tone_words[0]}, {tone_words[1]} sound that's instantly inspiring. Plus, it's got this {tone_words[2]} character that's become my secret weapon for standout tones.",
            
            f"The {pedal.name} isn't trying to reinvent the wheel - it's just doing it better than most. You get this {tone_words[0]} quality that's perfect for modern tones, but there's also a {tone_words[1]} element that keeps things musical. And when you need it, that {tone_words[2]} character is there to take things over the top.",
            
            f"I've got to say, the {pedal.name} surprised me. At first glance, it might look like just another {pedal.pedal_type.name.lower()} pedal, but plug it in and you're hit with this {tone_words[0]}, {tone_words[1]} sound that's addictive. The way it can go from subtle to {tone_words[2]} is just incredible.",
            
            f"What makes the {pedal.name} stand out? It starts with the {tone_words[0]} character - something you don't find in your average pedal. Add in the {tone_words[1]} response that feels so natural, and top it off with that {tone_words[2]} quality when you push it... it's a winner.",
        ]
        return random.choice(templates)

    def generate_my_experience(self, pedal):
        contexts = [
            "studio sessions",
            "live gigs",
            "band practice",
            "recording sessions",
            "jam sessions",
            "rehearsals",
            "bedroom practice",
            "songwriting sessions"
        ]
        
        # Use the pedal's actual genres from Best For if available
        genres = [g.strip() for g in pedal.best_for.split(",")] if pedal.best_for else [
            "blues",
            "rock",
            "metal",
            "jazz",
            "country",
            "indie",
            "ambient",
            "funk",
            "fusion",
            "prog"
        ]
        
        scenarios = [
            f"I've been putting the {pedal.name} through its paces in {random.choice(contexts)} and {random.choice(contexts)}",
            f"After extensive testing with the {pedal.name} in everything from {random.choice(contexts)} to {random.choice(contexts)}",
            f"I've had the {pedal.name} on my board for a while now, using it heavily in {random.choice(contexts)}",
            f"The {pedal.name} has been my go-to for {random.choice(contexts)} lately"
        ]
        
        # Use actual genres from the pedal data
        impressions = [
            f"and it's consistently impressed me with its versatility. Whether I'm playing {random.choice(genres)} or {random.choice(genres)}, it delivers exactly what I need.",
            f"and I've got to say, it's exceeded my expectations. It especially shines in {random.choice(genres)} and {random.choice(genres)} contexts.",
            f"and it's quickly become one of my favorite pedals. It's particularly great for {random.choice(genres)} stuff, but versatile enough for any style.",
            f"and it's proven itself time and time again. From subtle {random.choice(genres)} textures to full-on {random.choice(genres)} mayhem, it handles it all."
        ]
        
        details = [
            "The controls are intuitive, the sound quality is top-notch, and it plays nice with other pedals.",
            "What really stands out is the build quality and attention to detail - this thing is built to last.",
            "The range of sounds you can get from this pedal is impressive, and they're all usable in real-world situations.",
            "It's one of those pedals that makes you want to keep playing - there's always another sweet spot to discover."
        ]
        
        return f"{random.choice(scenarios)} {random.choice(impressions)} {random.choice(details)}"

    def handle(self, *args, **kwargs):
        pedals = Pedal.objects.all()
        
        for pedal in pedals:
            # Only update what_makes_it_good and my_experience
            # Leave main_features and best_for unchanged from your CSV data
            what_makes_it_good = self.generate_what_makes_it_good(pedal)
            my_experience = self.generate_my_experience(pedal)
            
            pedal.what_makes_it_good = what_makes_it_good
            pedal.my_experience = my_experience
            pedal.save()
            
            self.stdout.write(self.style.SUCCESS(f'Generated content for {pedal.name}'))
