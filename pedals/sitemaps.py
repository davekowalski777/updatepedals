from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Pedal

class PedalSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return Pedal.objects.all()

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return reverse('pedals:pedal_detail', args=[obj.slug])

class StaticSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.8

    def items(self):
        return [
            'pedals:home',
            'pedals:about',
            'pedals:manufacturer_list',
            'pedals:pedal_list',
            'pedals:pedals_for_beginners',
            'pedals:are_pedals_necessary',
            'pedals:what_are_guitar_pedals',
            'pedals:how_to_choose_guitar_pedals',
            'pedals:guitar_pedal_chain',
            'pedals:privacy_policy'
        ]

    def location(self, item):
        return reverse(item)
