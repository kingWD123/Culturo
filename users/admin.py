from django.contrib import admin
from .models import CulturalProfile, Destination, CulturalHighlight, Itinerary, ItineraryDay, ItineraryItem

@admin.register(CulturalProfile)
class CulturalProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'adventure_level', 'budget_level', 'travel_style', 'created_at']
    list_filter = ['budget_level', 'travel_style', 'created_at']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Utilisateur', {
            'fields': ('user',)
        }),
        ('Préférences Musicales', {
            'fields': ('preferred_music_genres',)
        }),
        ('Préférences Cinématographiques', {
            'fields': ('preferred_film_genres',)
        }),
        ('Préférences Culinaires', {
            'fields': ('preferred_cuisine_types',)
        }),
        ('Activités Culturelles', {
            'fields': ('preferred_activities',)
        }),
        ('Style de Voyage', {
            'fields': ('adventure_level', 'budget_level', 'travel_style')
        }),
        ('Métadonnées', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'country', 'average_cost', 'created_at']
    list_filter = ['country', 'average_cost', 'created_at']
    search_fields = ['name', 'city', 'country', 'description']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Informations de base', {
            'fields': ('name', 'country', 'city', 'description')
        }),
        ('Coordonnées', {
            'fields': ('latitude', 'longitude'),
            'classes': ('collapse',)
        }),
        ('Caractéristiques culturelles', {
            'fields': ('cultural_tags', 'music_scene', 'film_culture', 'culinary_highlights', 'cultural_activities')
        }),
        ('Médias', {
            'fields': ('main_image', 'gallery_images')
        }),
        ('Informations pratiques', {
            'fields': ('best_time_to_visit', 'average_cost')
        }),
        ('Métadonnées', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(CulturalHighlight)
class CulturalHighlightAdmin(admin.ModelAdmin):
    list_display = ['name', 'destination', 'category', 'price_range']
    list_filter = ['category', 'price_range', 'destination__country']
    search_fields = ['name', 'description', 'destination__city']
    
    fieldsets = (
        ('Informations de base', {
            'fields': ('destination', 'name', 'category', 'description')
        }),
        ('Localisation', {
            'fields': ('address', 'website')
        }),
        ('Caractéristiques', {
            'fields': ('cultural_tags', 'price_range', 'opening_hours')
        }),
        ('Médias', {
            'fields': ('image',)
        }),
    )

class ItineraryItemInline(admin.TabularInline):
    model = ItineraryItem
    extra = 1
    fields = ['highlight', 'title', 'description', 'start_time', 'end_time', 'activity_type', 'order']

class ItineraryDayInline(admin.TabularInline):
    model = ItineraryDay
    extra = 1
    fields = ['day_number', 'date', 'title', 'description']
    inlines = [ItineraryItemInline]

@admin.register(Itinerary)
class ItineraryAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'destination', 'start_date', 'end_date', 'status', 'cultural_match_score']
    list_filter = ['status', 'start_date', 'destination__country']
    search_fields = ['title', 'user__username', 'destination__city']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Informations de base', {
            'fields': ('user', 'destination', 'title', 'description')
        }),
        ('Dates', {
            'fields': ('start_date', 'end_date')
        }),
        ('Statut', {
            'fields': ('status', 'cultural_match_score')
        }),
        ('Métadonnées', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [ItineraryDayInline]

@admin.register(ItineraryDay)
class ItineraryDayAdmin(admin.ModelAdmin):
    list_display = ['itinerary', 'day_number', 'date', 'title']
    list_filter = ['date', 'itinerary__destination']
    search_fields = ['title', 'description', 'itinerary__title']
    
    inlines = [ItineraryItemInline]

@admin.register(ItineraryItem)
class ItineraryItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'day', 'activity_type', 'start_time', 'end_time', 'order']
    list_filter = ['activity_type', 'day__itinerary__destination']
    search_fields = ['title', 'description']
    ordering = ['day__day_number', 'order']
