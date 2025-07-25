# Culturo

Culturo is an immersive web platform for cultural recommendations around cinema, music, books, gastronomy and cultural events, focused on discovering atmospheres, local contexts and cultural ecosystems, without being limited to physical places.

## Objectives
- Provide personalized and immersive cultural recommendations.
- Associate films and music with local atmospheres or cultural contexts.
- Suggest thematic playlists according to popular genres or moments.
- Recommend books and documentaries on local history and culture.
- Allow "traveling" from home through works typical of a destination.
- Offer an enriched local cultural ecosystem: artist profiles, events, works, discovery advice.

## Main Features
- **Immersive recommendations**: works associated with atmospheres, contexts or destinations.
- **Thematic playlists**: music, films, readings according to themes or genres.
- **Local discovery**: books, documentaries, recipes, artists, events by region/country.
- **Artist profiles**: detailed profiles of local artists.
- **Personalized suggestions**: recommendations according to the user's cultural tastes.
- **Cultural calendar**: agenda of festivals, shows, events by region/country.
- **Discovery advice**: ideas for cultural activities at home or while traveling.

## Technical Structure
- Django (backend, models, views, templates)
- Main models: UserProfile, Artist, Work (Film, Music, Book, Recipe), Event, Playlist, CulturalAdvice

## Main Pages
- Immersive home page (exploration by atmosphere, destination, theme)
- User cultural profiles
- Artist/work/event profiles
- Thematic playlists
- Cultural calendar
- Discovery advice

## Installation
1. Clone the repository
2. Install Python dependencies
3. Run Django migrations
4. Start the development server

## Contribution
Any contribution is welcome to enrich the cultural database and improve the immersive experience!

## ✨ Features

### 🎯 Personalized Cultural Profile
- **Musical preferences**: Jazz, Rock, Classical, Electronic, etc.
- **Cinematographic tastes**: Drama, Comedy, Documentary, Art House, etc.
- **Culinary flavors**: Italian, Japanese, Street Food, Fine Dining, etc.
- **Cultural activities**: Museums, Theater, Festivals, Art Galleries, etc.
- **Travel style**: Relaxed, Active, Cultural, Adventurous, Luxury
- **Adventure level**: Scale from 1 to 10
- **Budget**: Economic, Moderate, Luxury

### 🤖 Intelligent AI Algorithm
- Analysis of cultural preferences
- Calculation of compatibility scores (0-100%)
- Personalized recommendations
- Ready for Qloo Taste AI™ integration

### 🗺️ Cultural Destinations
- **New Orleans**: Jazz, Creole cuisine, Mardi Gras
- **Paris**: Art, gastronomy, museums
- **Tokyo**: Technology, temples, Japanese cuisine
- **Barcelona**: Modernist architecture, Catalan culture
- **Istanbul**: History, Ottoman cuisine, mixed culture
- **Marrakech**: Souks, riads, Arab-Berber culture

### 📅 Personalized Itineraries
- Automatic itinerary generation
- Authentic cultural activities
- Day-by-day planning
- Local points of interest

## 🚀 Installation

### Prerequisites
- Python 3.8+
- Django 4.2+
- SQLite (default) or PostgreSQL

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/your-username/culturo.git
cd culturo
```

2. **Create a virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure the database**
```bash
python manage.py makemigrations
python manage.py migrate
```

5. **Create a superuser**
```bash
python manage.py createsuperuser
```

6. **Start the development server**
```bash
python manage.py runserver
```

7. **Access the application**
- Website: http://localhost:8000
- Admin: http://localhost:8000/admin

## 🏗️ Architecture

### Data Models

#### `CulturalProfile`
- User's cultural profile
- Musical, cinematographic, culinary preferences
- Travel style and adventure level

#### `Destination`
- Destinations with cultural characteristics
- Cultural tags, music scenes, local cuisine
- Images and practical information

#### `CulturalHighlight`
- Specific cultural points of interest
- Restaurants, museums, clubs, galleries
- Detailed information and schedules

#### `Itinerary`
- Personalized itineraries
- Cultural compatibility score
- Status and travel dates

#### `ItineraryDay` & `ItineraryItem`
- Detailed itinerary structure
- Activities by day with schedules
- Activity types (visit, meal, transport)

### Technologies Used

#### Frontend
- **Tailwind CSS**: Utility CSS framework
- **Alpine.js**: Lightweight JavaScript framework
- **Font Awesome**: Icons
- **Google Fonts**: Typography (Inter)

#### Backend
- **Django 4.2**: Python web framework
- **SQLite**: Database (development)
- **Django Admin**: Administration interface

#### Advanced Features
- **CSS Animations**: Smooth transitions
- **Intersection Observer**: Scroll animations
- **REST API**: Cultural compatibility calculation
- **Responsive Design**: Mobile-first

## 🎨 Design System

### Colors
- **Primary**: Gradient purple-600 to blue-600
- **Secondary**: Gray-50 to Gray-900
- **Accent**: Purple-500, Blue-500

### Typography
- **Main font**: Inter (Google Fonts)
- **Hierarchy**: text-5xl to text-sm
- **Weights**: 300, 400, 500, 600, 700, 800

### Components
- **Cards**: Rounded-2xl, shadow-lg, hover effects
- **Buttons**: Gradient backgrounds, rounded-full
- **Forms**: Modern checkboxes, custom sliders
- **Navigation**: Sticky, responsive, dropdown menus

## 🔧 Configuration

### Environment Variables
```bash
# settings.py
SECRET_KEY = 'your-secret-key'
DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

### Static Files
```bash
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
```

## 📱 Usage

### 1. Create a Cultural Profile
- Access `/profile/`
- Select your preferences in each category
- Define your travel style and budget
- Save your profile

### 2. Receive Recommendations
- Visit `/recommendations/`
- Discover destinations that match your profile
- View cultural compatibility scores

### 3. Explore a Destination
- Click "Discover" to see details
- Browse cultural points of interest
- Discover the music and culinary scene

### 4. Create an Itinerary
- Click "Plan" to create an itinerary
- Set your travel dates
- Receive a personalized schedule

## 🔮 Roadmap

### Phase 1 - MVP ✅
- [x] Data models
- [x] Modern user interface
- [x] Basic recommendation algorithm
- [x] Itinerary creation

### Phase 2 - Advanced AI 🚧
- [ ] Qloo Taste AI™ integration
- [ ] Review sentiment analysis
- [ ] Real-time recommendations
- [ ] Machine learning

### Phase 3 - Social Features 📅
- [ ] Itinerary sharing
- [ ] Traveler community
- [ ] Reviews and ratings
- [ ] Photos and stories

### Phase 4 - Expansion 📅
- [ ] Mobile application
- [ ] Integrated bookings
- [ ] Cultural audio guide
- [ ] Immersive AR/VR experiences

## 🤝 Contribution

We welcome contributions! Here's how to participate:

1. **Fork** the project
2. **Create** a branch for your feature
3. **Commit** your changes
4. **Push** to the branch
5. **Open** a Pull Request

### Guidelines
- Follow PEP 8 conventions for Python
- Use descriptive variable names
- Add tests for new features
- Document your code

## 📄 License

This project is under MIT license. See the `LICENSE` file for more details.

## 🙏 Acknowledgments

- **Qloo** for Taste AI™
- **Unsplash** for images
- **Tailwind CSS** for the CSS framework
- **Alpine.js** for JavaScript interactions
- **Django** for the web framework

## 📞 Contact

- **Email**: contact@culturo.com
- **Website**: https://culturo.com
- **Twitter**: @culturo_app
- **Instagram**: @culturo_app

---

**Culturo** - Transform your passion into a passport 🌍✨