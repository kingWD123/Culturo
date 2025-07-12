from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class CulturalProfile(models.Model):
    """Profil culturel de l'utilisateur basé sur ses goûts et préférences"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cultural_profile')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Préférences musicales
    MUSIC_GENRES = [
        ('jazz', 'Jazz'),
        ('rock', 'Rock'),
        ('classical', 'Classical'),
        ('electronic', 'Electronic'),
        ('folk', 'Folk'),
        ('hip_hop', 'Hip Hop'),
        ('world', 'World Music'),
        ('blues', 'Blues'),
        ('reggae', 'Reggae'),
        ('pop', 'Pop'),
    ]
    
    # Préférences cinématographiques
    FILM_GENRES = [
        ('drama', 'Drama'),
        ('comedy', 'Comedy'),
        ('action', 'Action'),
        ('documentary', 'Documentary'),
        ('art_house', 'Art House'),
        ('thriller', 'Thriller'),
        ('romance', 'Romance'),
        ('sci_fi', 'Science Fiction'),
        ('horror', 'Horror'),
        ('animation', 'Animation'),
    ]
    
    # Préférences culinaires
    CUISINE_TYPES = [
        ('italian', 'Italian'),
        ('french', 'French'),
        ('japanese', 'Japanese'),
        ('indian', 'Indian'),
        ('mexican', 'Mexican'),
        ('thai', 'Thai'),
        ('mediterranean', 'Mediterranean'),
        ('street_food', 'Street Food'),
        ('fine_dining', 'Fine Dining'),
        ('vegetarian', 'Vegetarian'),
    ]
    
    # Activités culturelles
    CULTURAL_ACTIVITIES = [
        ('museums', 'Museums & Galleries'),
        ('theater', 'Theater & Performance'),
        ('festivals', 'Festivals & Events'),
        ('bookstores', 'Bookstores & Libraries'),
        ('live_music', 'Live Music Venues'),
        ('art_galleries', 'Art Galleries'),
        ('historical_sites', 'Historical Sites'),
        ('local_markets', 'Local Markets'),
        ('parks', 'Parks & Nature'),
        ('architecture', 'Architecture'),
    ]
    
    # Champs de préférences
    preferred_music_genres = models.JSONField(default=list)
    preferred_film_genres = models.JSONField(default=list)
    preferred_cuisine_types = models.JSONField(default=list)
    preferred_activities = models.JSONField(default=list)
    
    # Niveau d'aventure (1-10)
    adventure_level = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        default=5
    )
    
    # Budget préféré
    BUDGET_LEVELS = [
        ('budget', 'Budget'),
        ('moderate', 'Moderate'),
        ('luxury', 'Luxury'),
    ]
    budget_level = models.CharField(max_length=10, choices=BUDGET_LEVELS, default='moderate')
    
    # Style de voyage
    TRAVEL_STYLES = [
        ('relaxed', 'Relaxed'),
        ('active', 'Active'),
        ('cultural', 'Cultural'),
        ('adventure', 'Adventure'),
        ('luxury', 'Luxury'),
    ]
    travel_style = models.CharField(max_length=20, choices=TRAVEL_STYLES, default='cultural')
    
    def __str__(self):
        return f"Cultural Profile for {self.user.username}"

class Destination(models.Model):
    """Destinations avec leurs caractéristiques culturelles"""
    name = models.CharField(max_length=200)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    description = models.TextField()
    
    # Coordonnées géographiques
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    
    # Caractéristiques culturelles
    cultural_tags = models.JSONField(default=list)  # Tags culturels (jazz, art, food, etc.)
    music_scene = models.TextField(blank=True)
    film_culture = models.TextField(blank=True)
    culinary_highlights = models.TextField(blank=True)
    cultural_activities = models.JSONField(default=list)
    
    # Images et médias
    main_image = models.URLField(blank=True)
    gallery_images = models.JSONField(default=list)
    
    # Informations pratiques
    best_time_to_visit = models.CharField(max_length=100, blank=True)
    average_cost = models.CharField(max_length=50, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.city}, {self.country}"

class CulturalHighlight(models.Model):
    """Points d'intérêt culturels spécifiques"""
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='highlights')
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=50)  # restaurant, venue, museum, etc.
    description = models.TextField()
    address = models.TextField(blank=True)
    website = models.URLField(blank=True)
    image = models.URLField(blank=True)
    
    # Caractéristiques culturelles
    cultural_tags = models.JSONField(default=list)
    price_range = models.CharField(max_length=20, blank=True)
    opening_hours = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.name} - {self.destination.city}"

class Itinerary(models.Model):
    """Itinéraire personnalisé pour un utilisateur"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='itineraries')
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='itineraries')
    title = models.CharField(max_length=200)
    description = models.TextField()
    
    # Dates
    start_date = models.DateField()
    end_date = models.DateField()
    
    # Statut
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('planned', 'Planned'),
        ('completed', 'Completed'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    
    # Score de compatibilité culturelle (0-100)
    cultural_match_score = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        default=0
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title} - {self.destination.city}"

class ItineraryDay(models.Model):
    """Journée spécifique dans un itinéraire"""
    itinerary = models.ForeignKey(Itinerary, on_delete=models.CASCADE, related_name='days')
    day_number = models.IntegerField()
    date = models.DateField()
    title = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    
    class Meta:
        ordering = ['day_number']
    
    def __str__(self):
        return f"Day {self.day_number} - {self.itinerary.title}"

class ItineraryItem(models.Model):
    """Élément spécifique dans une journée d'itinéraire"""
    day = models.ForeignKey(ItineraryDay, on_delete=models.CASCADE, related_name='items')
    highlight = models.ForeignKey(CulturalHighlight, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    order = models.IntegerField(default=0)
    
    # Type d'activité
    ACTIVITY_TYPES = [
        ('visit', 'Visit'),
        ('meal', 'Meal'),
        ('activity', 'Activity'),
        ('transport', 'Transport'),
        ('rest', 'Rest'),
    ]
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPES, default='visit')
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.title} - Day {self.day.day_number}"

# ================= NOUVEAUX MODELES CULTURO ===================

class Artiste(models.Model):
    """Profil d'artiste local (musicien, réalisateur, auteur, chef, etc.)"""
    nom = models.CharField(max_length=200)
    bio = models.TextField()
    pays = models.CharField(max_length=100)
    region = models.CharField(max_length=100, blank=True)
    photo = models.URLField(blank=True)
    site_web = models.URLField(blank=True)
    def __str__(self):
        return self.nom

class Oeuvre(models.Model):
    """Oeuvre culturelle : Film, Musique, Livre, Recette"""
    TYPES = [
        ('film', 'Film'),
        ('musique', 'Musique'),
        ('livre', 'Livre'),
        ('recette', 'Recette'),
    ]
    titre = models.CharField(max_length=200)
    type = models.CharField(max_length=20, choices=TYPES)
    description = models.TextField()
    ambiance = models.CharField(max_length=200, blank=True)  # ex: "soirée jazz à Paris"
    contexte = models.CharField(max_length=200, blank=True)
    artiste = models.ForeignKey(Artiste, on_delete=models.SET_NULL, null=True, blank=True, related_name='oeuvres')
    pays = models.CharField(max_length=100, blank=True)
    region = models.CharField(max_length=100, blank=True)
    lien = models.URLField(blank=True)  # lien vers l'oeuvre (streaming, fiche, etc.)
    image = models.URLField(blank=True)
    def __str__(self):
        return f"{self.titre} ({self.get_type_display()})"

class Evenement(models.Model):
    """Evénement culturel (festival, spectacle, etc.)"""
    nom = models.CharField(max_length=200)
    type = models.CharField(max_length=100)
    date = models.DateField()
    lieu = models.CharField(max_length=200)
    description = models.TextField()
    artistes = models.ManyToManyField(Artiste, blank=True, related_name='evenements')
    pays = models.CharField(max_length=100)
    region = models.CharField(max_length=100, blank=True)
    site_web = models.URLField(blank=True)
    image = models.URLField(blank=True)
    def __str__(self):
        return f"{self.nom} - {self.pays}"

class Playlist(models.Model):
    """Playlist thématique (musique, films, lectures)"""
    THEME_CHOICES = [
        ('voyage', 'Voyage'),
        ('soirée', 'Soirée'),
        ('lecture', 'Lecture'),
        ('découverte', 'Découverte'),
        ('autre', 'Autre'),
    ]
    titre = models.CharField(max_length=200)
    theme = models.CharField(max_length=50, choices=THEME_CHOICES, default='autre')
    description = models.TextField(blank=True)
    oeuvres = models.ManyToManyField(Oeuvre, blank=True, related_name='playlists')
    pays = models.CharField(max_length=100, blank=True)
    region = models.CharField(max_length=100, blank=True)
    image = models.URLField(blank=True)
    def __str__(self):
        return self.titre

class ConseilCulturel(models.Model):
    """Conseil de découverte culturelle à domicile ou en voyage"""
    TYPE_CHOICES = [
        ('domicile', 'À domicile'),
        ('voyage', 'En voyage'),
    ]
    texte = models.TextField()
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    pays = models.CharField(max_length=100, blank=True)
    region = models.CharField(max_length=100, blank=True)
    def __str__(self):
        return f"Conseil {self.get_type_display()} - {self.pays or 'Général'}"
