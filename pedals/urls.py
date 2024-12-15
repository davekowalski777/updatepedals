from django.urls import path, re_path
from . import views
from django.conf import settings
from django.views.static import serve

app_name = 'pedals'

urlpatterns = [
    path('', views.home, name='home'),
    path('pedals/', views.PedalListView.as_view(), name='pedal_list'),
    path('pedal/<slug:slug>/', views.PedalDetailView.as_view(), name='pedal_detail'),
    path('manufacturers/', views.manufacturer_list, name='manufacturer_list'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('pedal/<slug:slug>/rate/', views.RateView.as_view(), name='rate_pedal'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('guides/pedals-for-beginners/', views.pedals_for_beginners, name='pedals_for_beginners'),
    path('guides/are-pedals-necessary/', views.are_pedals_necessary, name='are_pedals_necessary'),
    path('guides/what-are-guitar-pedals/', views.what_are_guitar_pedals, name='what_are_guitar_pedals'),
    path('guides/how-to-choose-guitar-pedals/', views.how_to_choose_guitar_pedals, name='how_to_choose_guitar_pedals'),
    path('guides/guitar-pedal-chain/', views.guitar_pedal_chain, name='guitar_pedal_chain'),

    # Serve sitemap.xml from static files
    re_path(r'^sitemap\.xml$', serve, {
        'document_root': settings.STATIC_ROOT,
        'path': 'sitemap.xml',
    }),
]
