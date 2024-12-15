import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'guitar_pedals.settings_prod')

application = get_wsgi_application()
app = application  # Vercel needs the 'app' variable
