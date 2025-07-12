# Culturo

Culturo est une plateforme web immersive de recommandations culturelles autour du cinéma, de la musique, des livres, de la gastronomie et des événements culturels, axée sur la découverte d'ambiances, de contextes locaux et d'écosystèmes culturels, sans se limiter à des lieux physiques.

## Objectifs
- Proposer des recommandations culturelles personnalisées et immersives.
- Associer films et musiques à des ambiances ou contextes culturels locaux.
- Suggérer des playlists thématiques selon les genres populaires ou les moments.
- Recommander des livres et documentaires sur l'histoire et la culture locale.
- Permettre de "voyager" depuis chez soi grâce à des œuvres typiques d'une destination.
- Offrir un écosystème culturel local enrichi : profils d'artistes, événements, œuvres, conseils de découverte.

## Fonctionnalités principales
- **Recommandations immersives** : œuvres associées à des ambiances, contextes ou destinations.
- **Playlists thématiques** : musique, films, lectures selon des thèmes ou genres.
- **Découverte locale** : livres, documentaires, recettes, artistes, événements par région/pays.
- **Profils d'artistes** : fiches détaillées d'artistes locaux.
- **Suggestions personnalisées** : recommandations selon les goûts culturels de l'utilisateur.
- **Calendrier culturel** : agenda des festivals, spectacles, événements par région/pays.
- **Conseils de découverte** : idées d'activités culturelles à domicile ou en voyage.

## Structure technique
- Django (backend, modèles, vues, templates)
- Modèles principaux : UserProfile, Artiste, Œuvre (Film, Musique, Livre, Recette), Événement, Playlist, ConseilCulturel

## Pages principales
- Accueil immersive (exploration par ambiance, destination, thématique)
- Profils culturels utilisateurs
- Fiches artistes/œuvres/événements
- Playlists thématiques
- Calendrier culturel
- Conseils de découverte

## Installation
1. Cloner le dépôt
2. Installer les dépendances Python
3. Lancer les migrations Django
4. Démarrer le serveur de développement

## Contribution
Toute contribution est la bienvenue pour enrichir la base culturelle et améliorer l'expérience immersive !

## ✨ Fonctionnalités

### 🎯 Profil Culturel Personnalisé
- **Préférences musicales** : Jazz, Rock, Classique, Électronique, etc.
- **Goûts cinématographiques** : Drame, Comédie, Documentaire, Art House, etc.
- **Saveurs culinaires** : Italien, Japonais, Street Food, Fine Dining, etc.
- **Activités culturelles** : Musées, Théâtre, Festivals, Galeries d'art, etc.
- **Style de voyage** : Détendu, Actif, Culturel, Aventureux, Luxe
- **Niveau d'aventure** : Échelle de 1 à 10
- **Budget** : Économique, Modéré, Luxe

### 🤖 Algorithme IA Intelligent
- Analyse des préférences culturelles
- Calcul de scores de compatibilité (0-100%)
- Recommandations personnalisées
- Prêt pour l'intégration Qloo Taste AI™

### 🗺️ Destinations Culturelles
- **New Orleans** : Jazz, cuisine créole, Mardi Gras
- **Paris** : Art, gastronomie, musées
- **Tokyo** : Technologie, temples, cuisine japonaise
- **Barcelona** : Architecture moderniste, culture catalane
- **Istanbul** : Histoire, cuisine ottomane, culture mixte
- **Marrakech** : Souks, riads, culture arabo-berbère

### 📅 Itinéraires Personnalisés
- Génération automatique d'itinéraires
- Activités culturelles authentiques
- Planning jour par jour
- Points d'intérêt locaux

## 🚀 Installation

### Prérequis
- Python 3.8+
- Django 4.2+
- SQLite (par défaut) ou PostgreSQL

### Installation

1. **Cloner le repository**
```bash
git clone https://github.com/votre-username/culturo.git
cd culturo
```

2. **Créer un environnement virtuel**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

3. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

4. **Configurer la base de données**
```bash
python manage.py makemigrations
python manage.py migrate
```

5. **Créer un superutilisateur**
```bash
python manage.py createsuperuser
```

6. **Lancer le serveur de développement**
```bash
python manage.py runserver
```

7. **Accéder à l'application**
- Site web : http://localhost:8000
- Admin : http://localhost:8000/admin

## 🏗️ Architecture

### Modèles de Données

#### `CulturalProfile`
- Profil culturel de l'utilisateur
- Préférences musicales, cinématographiques, culinaires
- Style de voyage et niveau d'aventure

#### `Destination`
- Destinations avec caractéristiques culturelles
- Tags culturels, scènes musicales, cuisine locale
- Images et informations pratiques

#### `CulturalHighlight`
- Points d'intérêt culturels spécifiques
- Restaurants, musées, clubs, galeries
- Informations détaillées et horaires

#### `Itinerary`
- Itinéraires personnalisés
- Score de compatibilité culturelle
- Statut et dates de voyage

#### `ItineraryDay` & `ItineraryItem`
- Structure détaillée des itinéraires
- Activités par jour avec horaires
- Types d'activités (visite, repas, transport)

### Technologies Utilisées

#### Frontend
- **Tailwind CSS** : Framework CSS utilitaire
- **Alpine.js** : Framework JavaScript léger
- **Font Awesome** : Icônes
- **Google Fonts** : Typographie (Inter)

#### Backend
- **Django 4.2** : Framework web Python
- **SQLite** : Base de données (développement)
- **Django Admin** : Interface d'administration

#### Fonctionnalités Avancées
- **Animations CSS** : Transitions fluides
- **Intersection Observer** : Animations au scroll
- **API REST** : Calcul de compatibilité culturelle
- **Responsive Design** : Mobile-first

## 🎨 Design System

### Couleurs
- **Primaire** : Gradient purple-600 à blue-600
- **Secondaire** : Gray-50 à Gray-900
- **Accent** : Purple-500, Blue-500

### Typographie
- **Police principale** : Inter (Google Fonts)
- **Hiérarchie** : text-5xl à text-sm
- **Poids** : 300, 400, 500, 600, 700, 800

### Composants
- **Cartes** : Rounded-2xl, shadow-lg, hover effects
- **Boutons** : Gradient backgrounds, rounded-full
- **Formulaires** : Modern checkboxes, sliders personnalisés
- **Navigation** : Sticky, responsive, dropdown menus

## 🔧 Configuration

### Variables d'Environnement
```bash
# settings.py
SECRET_KEY = 'votre-secret-key'
DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Base de données
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

### Fichiers Statiques
```bash
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
```

## 📱 Utilisation

### 1. Créer un Profil Culturel
- Accédez à `/profile/`
- Sélectionnez vos préférences dans chaque catégorie
- Définissez votre style de voyage et budget
- Sauvegardez votre profil

### 2. Recevoir des Recommandations
- Consultez `/recommendations/`
- Découvrez les destinations qui correspondent à votre profil
- Voir les scores de compatibilité culturelle

### 3. Explorer une Destination
- Cliquez sur "Découvrir" pour voir les détails
- Consultez les points d'intérêt culturels
- Découvrez la scène musicale et culinaire

### 4. Créer un Itinéraire
- Cliquez sur "Planifier" pour créer un itinéraire
- Définissez vos dates de voyage
- Recevez un planning personnalisé

## 🔮 Roadmap

### Phase 1 - MVP ✅
- [x] Modèles de données
- [x] Interface utilisateur moderne
- [x] Algorithme de recommandation basique
- [x] Création d'itinéraires

### Phase 2 - IA Avancée 🚧
- [ ] Intégration Qloo Taste AI™
- [ ] Analyse de sentiment des avis
- [ ] Recommandations en temps réel
- [ ] Apprentissage automatique

### Phase 3 - Fonctionnalités Sociales 📅
- [ ] Partage d'itinéraires
- [ ] Communauté de voyageurs
- [ ] Avis et notes
- [ ] Photos et stories

### Phase 4 - Expansion 📅
- [ ] Application mobile
- [ ] Réservations intégrées
- [ ] Guide audio culturel
- [ ] Expériences immersives AR/VR

## 🤝 Contribution

Nous accueillons les contributions ! Voici comment participer :

1. **Fork** le projet
2. **Créez** une branche pour votre fonctionnalité
3. **Commitez** vos changements
4. **Poussez** vers la branche
5. **Ouvrez** une Pull Request

### Guidelines
- Suivez les conventions PEP 8 pour Python
- Utilisez des noms de variables descriptifs
- Ajoutez des tests pour les nouvelles fonctionnalités
- Documentez votre code

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 🙏 Remerciements

- **Qloo** pour Taste AI™
- **Unsplash** pour les images
- **Tailwind CSS** pour le framework CSS
- **Alpine.js** pour les interactions JavaScript
- **Django** pour le framework web

## 📞 Contact

- **Email** : contact@culturo.com
- **Site web** : https://culturo.com
- **Twitter** : @culturo_app
- **Instagram** : @culturo_app

---

**Culturo** - Transformez votre passion en passeport 🌍✨ 