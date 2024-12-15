from django.contrib import admin
from .models import Manufacturer, PedalType, Pedal, Comment, Author

# Register your models here.

@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ('name', 'website')
    search_fields = ('name',)

@admin.register(PedalType)
class PedalTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Pedal)
class PedalAdmin(admin.ModelAdmin):
    list_display = ('name', 'manufacturer', 'pedal_type', 'my_rating')
    list_filter = ('manufacturer', 'pedal_type')
    search_fields = ('name', 'manufacturer__name')
    prepopulated_fields = {'slug': ('name',)}
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'manufacturer', 'pedal_type', 'image_url', 'affiliate_link', 'price')
        }),
        ('Content', {
            'fields': ('what_makes_it_good', 'what_makes_it_bad', 'best_for', 'my_experience', 'specifications')
        }),
        ('Custom Section Headings', {
            'fields': ('heading_what_makes_it_good', 'heading_best_for', 'heading_my_experience', 'heading_specifications'),
            'classes': ('collapse',),
            'description': 'Customize the section headings for this pedal. Leave blank to use defaults.'
        }),
        ('Metadata', {
            'fields': ('my_rating', 'meta_description', 'author'),
            'classes': ('collapse',)
        })
    )

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author_name', 'pedal', 'created_at', 'is_approved')
    list_filter = ('is_approved', 'created_at')
    search_fields = ('author_name', 'email', 'content', 'pedal__name')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)
    approve_comments.short_description = "Approve selected comments"
