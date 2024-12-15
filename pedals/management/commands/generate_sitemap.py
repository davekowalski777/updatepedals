from django.core.management.base import BaseCommand
from django.urls import reverse
from pedals.models import Pedal, Manufacturer, PedalType
from datetime import datetime
import xml.etree.ElementTree as ET
import os

class Command(BaseCommand):
    help = 'Generates a sitemap.xml file'

    def handle(self, *args, **options):
        # Create the root element
        urlset = ET.Element('urlset')
        urlset.set('xmlns', 'http://www.sitemaps.org/schemas/sitemap/0.9')

        # Base URL
        base_url = 'https://guitarpedals.com'

        # Add static pages
        static_pages = [
            ('/', 'daily', '1.0'),
            ('/pedals/', 'daily', '0.9'),
            ('/manufacturers/', 'weekly', '0.8'),
            ('/about/', 'monthly', '0.7'),
            ('/guides/what-are-guitar-pedals/', 'weekly', '0.9'),
            ('/guides/how-to-choose-guitar-pedals/', 'weekly', '0.9'),
            ('/guides/guitar-pedal-chain/', 'weekly', '0.9'),
            ('/guides/pedals-for-beginners/', 'weekly', '0.9'),
            ('/guides/are-pedals-necessary/', 'weekly', '0.9'),
        ]

        # Add static pages to sitemap
        for path, freq, priority in static_pages:
            url = ET.SubElement(urlset, 'url')
            loc = ET.SubElement(url, 'loc')
            loc.text = f"{base_url}{path}"
            changefreq = ET.SubElement(url, 'changefreq')
            changefreq.text = freq
            priority_elem = ET.SubElement(url, 'priority')
            priority_elem.text = priority

        # Add all pedal pages
        pedals = Pedal.objects.all()
        for pedal in pedals:
            url = ET.SubElement(urlset, 'url')
            loc = ET.SubElement(url, 'loc')
            loc.text = f"{base_url}/pedal/{pedal.slug}/"
            lastmod = ET.SubElement(url, 'lastmod')
            lastmod.text = datetime.now().strftime('%Y-%m-%d')
            changefreq = ET.SubElement(url, 'changefreq')
            changefreq.text = 'weekly'
            priority_elem = ET.SubElement(url, 'priority')
            priority_elem.text = '0.8'

        # Add manufacturer pages
        manufacturers = Manufacturer.objects.all()
        for manufacturer in manufacturers:
            url = ET.SubElement(urlset, 'url')
            loc = ET.SubElement(url, 'loc')
            loc.text = f"{base_url}/manufacturers/{manufacturer.name.lower().replace(' ', '-')}/"
            lastmod = ET.SubElement(url, 'lastmod')
            lastmod.text = datetime.now().strftime('%Y-%m-%d')
            changefreq = ET.SubElement(url, 'changefreq')
            changefreq.text = 'weekly'
            priority_elem = ET.SubElement(url, 'priority')
            priority_elem.text = '0.8'

        # Add pedal type pages
        pedal_types = PedalType.objects.all()
        for pedal_type in pedal_types:
            url = ET.SubElement(urlset, 'url')
            loc = ET.SubElement(url, 'loc')
            loc.text = f"{base_url}/pedals/type/{pedal_type.name.lower().replace(' ', '-')}/"
            lastmod = ET.SubElement(url, 'lastmod')
            lastmod.text = datetime.now().strftime('%Y-%m-%d')
            changefreq = ET.SubElement(url, 'changefreq')
            changefreq.text = 'weekly'
            priority_elem = ET.SubElement(url, 'priority')
            priority_elem.text = '0.8'

        # Create the XML file
        tree = ET.ElementTree(urlset)
        
        # Get the project root directory
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
        
        # Write to sitemap.xml in the project root
        tree.write(os.path.join(project_root, 'sitemap.xml'), 
                  encoding='utf-8', 
                  xml_declaration=True,
                  method='xml')
        
        self.stdout.write(self.style.SUCCESS('Successfully generated sitemap.xml'))
