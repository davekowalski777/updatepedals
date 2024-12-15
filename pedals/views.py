from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.http import JsonResponse
from django.db.models import Avg, Q
from .models import Pedal, Manufacturer, PedalType, UserRating, Author
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from .forms import CommentForm

@cache_page(300)  # Cache for 5 minutes
def home(request):
    """View for the home page."""
    featured_pedals = list(Pedal.objects.all().order_by('-my_rating')[:6])
    return render(request, 'pedals/home.html', {
        'featured_pedals': featured_pedals,
    })

@cache_page(300)
def about(request):
    """View for the about page."""
    return render(request, 'about.html')

@cache_page(300)
def privacy_policy(request):
    """View for the privacy policy page."""
    return render(request, 'privacy_policy.html')

@cache_page(300)
def pedals_for_beginners(request):
    return render(request, 'guides/pedals_for_beginners.html')

@cache_page(300)
def are_pedals_necessary(request):
    return render(request, 'guides/are_pedals_necessary.html')

@cache_page(300)
def what_are_guitar_pedals(request):
    return render(request, 'guides/what_are_guitar_pedals.html')

@cache_page(300)
def how_to_choose_guitar_pedals(request):
    return render(request, 'guides/how_to_choose_guitar_pedals.html')

@cache_page(300)
def guitar_pedal_chain(request):
    return render(request, 'guides/guitar_pedal_chain.html')

def contact(request):
    """View function for the contact page."""
    return render(request, 'pedals/contact.html')

class PedalListView(ListView):
    model = Pedal
    template_name = 'pedals/pedal_list.html'
    context_object_name = 'pedals'
    paginate_by = 12

    def get_queryset(self):
        queryset = Pedal.objects.all()
        
        # Get filter parameters from GET request
        manufacturer_id = self.request.GET.get('manufacturer')
        pedal_type_id = self.request.GET.get('type')
        search_query = self.request.GET.get('search', '').strip()

        # Apply manufacturer filter
        if manufacturer_id:
            queryset = queryset.filter(manufacturer_id=manufacturer_id)
        
        # Apply pedal type filter
        if pedal_type_id:
            queryset = queryset.filter(pedal_type_id=pedal_type_id)

        # Apply search filter with multi-word support
        if search_query:
            # Split the search query into individual terms
            search_terms = search_query.split()
            
            # Create a query that matches all terms across different fields
            query = Q()
            for term in search_terms:
                term_query = (
                    Q(name__icontains=term) |
                    Q(manufacturer__name__icontains=term) |
                    Q(what_makes_it_good__icontains=term)
                )
                query &= term_query  # Use AND between terms
            
            queryset = queryset.filter(query)

        return queryset.select_related('manufacturer', 'pedal_type')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['manufacturers'] = Manufacturer.objects.all()
        context['pedal_types'] = PedalType.objects.all()
        context['selected_manufacturer'] = self.request.GET.get('manufacturer', '')
        context['selected_type'] = self.request.GET.get('type', '')
        context['search_query'] = self.request.GET.get('search', '')
        return context

class PedalDetailView(DetailView):
    model = Pedal
    template_name = 'pedals/pedal_detail.html'
    context_object_name = 'pedal'
    slug_url_kwarg = 'slug'
    
    def get_object(self, queryset=None):
        return super().get_object(queryset)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pedal = self.object
        
        # Get the default author
        if not pedal.author:
            author = Author.objects.get(name='Dave')
            pedal.author = author
            pedal.save()
        
        # Get average user rating
        avg_rating = pedal.user_ratings.aggregate(Avg('rating'))['rating__avg']
        context['average_user_rating'] = round(avg_rating, 1) if avg_rating else 0
        
        # Get user's previous rating if it exists
        if 'HTTP_X_FORWARDED_FOR' in self.request.META:
            ip = self.request.META['HTTP_X_FORWARDED_FOR'].split(',')[0]
        else:
            ip = self.request.META['REMOTE_ADDR']
        try:
            user_rating = pedal.user_ratings.get(ip_address=ip)
            context['user_rating'] = user_rating.rating
        except UserRating.DoesNotExist:
            context['user_rating'] = None
        
        # Get related pedals
        same_brand_pedals = Pedal.objects.filter(
            manufacturer=pedal.manufacturer
        ).exclude(
            id=pedal.id
        ).order_by('?')[:2]  # Random 2 pedals from same manufacturer
        
        same_type_pedals = Pedal.objects.filter(
            pedal_type=pedal.pedal_type
        ).exclude(
            id=pedal.id
        ).exclude(
            manufacturer=pedal.manufacturer  # Exclude same manufacturer to avoid duplicates
        ).order_by('?')[:2]  # Random 2 pedals of same type
        
        context['related_pedals'] = list(same_brand_pedals) + list(same_type_pedals)
        
        context['comment_form'] = CommentForm()
        context['comments'] = self.object.comments.filter(is_approved=True).select_related('pedal')
        
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)
        
        if form.is_valid():
            comment = form.save(commit=False)
            comment.pedal = self.object
            comment.ip_address = request.META.get('REMOTE_ADDR')
            comment.save()
            return JsonResponse({
                'status': 'success',
                'message': 'Your comment has been submitted and is awaiting approval.'
            })
        
        return JsonResponse({
            'status': 'error',
            'errors': form.errors
        }, status=400)

def manufacturer_list(request):
    manufacturers = Manufacturer.objects.all()
    return render(request, 'pedals/manufacturer_list.html', {'manufacturers': manufacturers})

@method_decorator(csrf_exempt, name='dispatch')
class RateView(DetailView):
    model = Pedal
    slug_url_kwarg = 'slug'
    
    def post(self, request, *args, **kwargs):
        pedal = self.get_object()
        rating = request.POST.get('rating')
        ip_address = request.META.get('REMOTE_ADDR')
        
        if rating and rating.isdigit():
            rating = int(rating)
            if 1 <= rating <= 5:
                UserRating.objects.update_or_create(
                    pedal=pedal,
                    ip_address=ip_address,
                    defaults={'rating': rating}
                )
                
                avg_rating = UserRating.objects.filter(pedal=pedal).aggregate(Avg('rating'))['rating__avg']
                return JsonResponse({'success': True, 'average_rating': avg_rating})
        
        return JsonResponse({'success': False}, status=400)
