from django.db import models
from django.utils.text import slugify

# Create your models here.

class Manufacturer(models.Model):
    name = models.CharField(max_length=100)
    website = models.URLField(blank=True)
    about = models.TextField(blank=True)  # Added for About Brand
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

class PedalType(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

class Author(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField()
    years_of_experience = models.IntegerField()
    profile_image = models.URLField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Pedal(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, related_name='pedals')
    pedal_type = models.ForeignKey(PedalType, on_delete=models.SET_NULL, null=True, related_name='pedals')
    what_makes_it_good = models.TextField(help_text="What makes this pedal good?", blank=True)  # Changed from description
    my_experience = models.TextField(blank=True)  # Changed from controls
    main_features = models.TextField(blank=True)
    what_makes_it_bad = models.TextField(help_text="What makes this pedal bad?", blank=True)
    my_rating = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    meta_description = models.TextField(max_length=160, blank=True, help_text="SEO meta description")
    specifications = models.TextField(blank=True, help_text="Technical specifications like power requirements, dimensions, input/output jacks, etc.")
    best_for = models.CharField(max_length=200, blank=True)
    image_url = models.URLField(blank=True, null=True)
    affiliate_link = models.URLField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    release_date = models.DateField(null=True, blank=True)
    is_discontinued = models.BooleanField(default=False)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, related_name='pedals')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Custom section headings
    heading_what_makes_it_good = models.CharField(max_length=100, blank=True, default="What Makes It Good")
    heading_best_for = models.CharField(max_length=100, blank=True, default="Best For")
    heading_my_experience = models.CharField(max_length=100, blank=True, default="My Experience")
    heading_specifications = models.CharField(max_length=100, blank=True, default="Specifications")
    
    def save(self, *args, **kwargs):
        if not self.slug:
            # Create slug from manufacturer name and pedal name
            base_slug = f"{self.manufacturer.name}-{self.name}"
            new_slug = slugify(base_slug) + "-review"
            # Handle potential duplicates by adding a number
            counter = 1
            temp_slug = new_slug
            while Pedal.objects.filter(slug=temp_slug).exists():
                temp_slug = f"{new_slug}-{counter}"
                counter += 1
            self.slug = temp_slug
        super().save(*args, **kwargs)

    def get_formatted_title(self):
        """Returns a formatted title for the pedal review"""
        return f"{self.manufacturer.name.upper()} {self.name} - Review, Features, Specs"

    def get_youtube_search_url(self):
        """Returns a YouTube search URL for the pedal"""
        search_query = f"{self.manufacturer.name} {self.name}"
        return f"https://www.youtube.com/results?search_query={search_query.replace(' ', '+')}"

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['manufacturer__name', 'name']

class Comment(models.Model):
    pedal = models.ForeignKey(Pedal, on_delete=models.CASCADE, related_name='comments')
    author_name = models.CharField(max_length=100)
    email = models.EmailField()
    content = models.TextField()
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)], default=5)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_approved = models.BooleanField(default=False)
    ip_address = models.GenericIPAddressField()

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Comment by {self.author_name} on {self.pedal.name}'

    @property
    def stars(self):
        return '★' * self.rating + '☆' * (5 - self.rating)

class UserRating(models.Model):
    pedal = models.ForeignKey(Pedal, on_delete=models.CASCADE, related_name='user_ratings')
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    ip_address = models.GenericIPAddressField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('pedal', 'ip_address')

    @property
    def stars(self):
        return '★' * self.rating + '☆' * (5 - self.rating)
