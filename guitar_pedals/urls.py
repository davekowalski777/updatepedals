from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pedals.urls')),
    path('robots.txt', TemplateView.as_view(template_name="robots.txt", 
         content_type="text/plain"), name='robots'),
]
