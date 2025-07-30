
# 🌍 Culturo - Intelligent Cultural Recommendations Platform

**Culturo** is an immersive web platform that **revolutionizes cultural discovery** by combining **artificial intelligence** with the **Qloo** and **Gemini APIs** to offer **personalized recommendations** for destinations, restaurants, hotels, and cinema.

Here is our [demo](https://youtu.be/KOBKu__Sg1E)
---

## 🎯 Project Vision

Culturo transforms how people discover and explore global culture by offering:

- **Intelligent recommendations** based on personal tastes and preferences  
- **Interactive exploration** with maps and AI-powered chatbots  
- **Immersive experiences** through a modern, responsive UI  
- **Authentic discovery** of destinations, gastronomy, and accommodations
- **User authentication system** with personalized experiences

---

## ✨ Key Features

### 🗺️ Destination Recommendations
- AI chatbot powered by **Gemini** for personalized suggestions  
- **Qloo API** integration for taste-based recommendations  
- **Interactive maps** with dynamic markers using Leaflet.js
- Default recommendations visible for all users
- Enhanced chatbot functionality for authenticated users
- Responsive design with smooth animations

### 🍽️ Gastronomic Discovery
- Personalized restaurant suggestions based on user preferences  
- Geolocation support for nearby options  
- Detailed restaurant info (cuisine, price, ratings)  
- **Interactive maps** with restaurant markers
- Default restaurant recommendations for all visitors
- AI chatbot for personalized dining suggestions

### 🏨 Quality Accommodations
- Hotel recommendations based on travel profiles  
- Support for major destinations worldwide
- **Interactive map interface** with hotel markers
- Default hotel suggestions available without login
- Personalized chatbot recommendations for authenticated users
- Filters by amenities, price, and location

### 🎬 Cinema Discovery
- Taste-driven movie suggestions  
- AI chatbot focused on cinema content  
- **Latest releases showcase** with movie cards
- **Event agenda** for cinema screenings and discussions
- Smooth and minimal UI with Netflix-inspired design
- Authentication-based chatbot access

---

## 🛠️ Technical Architecture

### 🔗 Integrated APIs
- **🤖 Gemini AI** – For chatbot conversations and natural language understanding  
- **🎯 Qloo API** – Cultural and taste-based recommendation engine  
- **📸 Unsplash API** – High-quality image integration

### 🎨 Frontend Technologies
- **HTML5 / CSS3** – Responsive, mobile-first layout  
- **Vanilla JavaScript** – Dynamic interactions with error handling
- **Leaflet.js** – Interactive maps with markers and layers  
- **Chat UI components** – For multiple chatbot interactions
- **Font Awesome** – Icon library for social media and UI elements

### 🔧 Backend Technologies
- **Django 4.2+** – Robust web framework
- **Django Authentication** – User management system
- **RESTful APIs** – For chatbot and recommendation endpoints
- **Error handling** – Comprehensive error management for API calls

### 🗂️ Enhanced Data Models
```python
# User authentication and profiles
User:
    - Django built-in user model
    - Authentication system integration

# Cultural destinations with enhanced features
Destination:
    - tags, description, cuisine, music scenes, location
    - Default recommendations for non-authenticated users

# Restaurant recommendations
Restaurant:
    - cuisine type, ratings, price range, location
    - Integration with maps and chatbot

# Hotel accommodations
Hotel:
    - amenities, price range, location, ratings
    - Map integration and filtering options

# Cinema content
Cinema:
    - movie recommendations, latest releases
    - event scheduling and agenda management
```

---

## 🚀 Installation & Setup

### ✅ Prerequisites
- Python 3.8+  
- Django 4.2+  
- API keys for Gemini, Qloo, and Unsplash

### 📦 Installation Steps

```bash
# 1. Clone the repository
git clone https://github.com/kingWD123/Culturo
cd culturo

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate      # On Unix/macOS
venv\Scripts\activate       # On Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Add your API keys in settings.py or a .env file
# Example (settings.py)
GEMINI_API_KEY = 'your_gemini_key'
CLOOAI_API_KEY = 'your_qloo_key'
UNSPLASH_ACCESS_KEY = 'your_unsplash_key'

# 5. Run migrations
python manage.py makemigrations
python manage.py migrate

# 6. Create a superuser (optional)
python manage.py createsuperuser

# 7. Start the development server
python manage.py runserver
```

### 🌐 Access the App
- App: [http://localhost:8000](http://localhost:8000)  
- Admin Panel: [http://localhost:8000/admin](http://localhost:8000/admin)

---

## 📱 User Guide

### 🏠 Home Page
- Immersive welcome UI with discovery sections  
- Quick access to destinations, food, hotels, and cinema
- User authentication options (login/register)

### 🌍 Destinations
- **For all users:** Default destination recommendations with interactive maps
- **For authenticated users:** AI chatbot for personalized suggestions
- Ask the chatbot: *"I want to visit Paris"* for tailored recommendations

### 🍴 Restaurants
- **Default recommendations** available for all visitors
- **Interactive map** showing restaurant locations
- **For logged-in users:** Personalized chatbot suggestions
- Ask: *"Find restaurants in Tokyo"* for curated suggestions

### 🏨 Hotels
- **Default hotel suggestions** with map integration
- **For authenticated users:** Personalized chatbot recommendations
- Filter by preference, price, and location
- Interactive map with hotel markers

### 🎥 Cinema
- **Latest releases** showcase for all users
- **Cinema agenda** with events and screenings
- **For authenticated users:** AI chatbot for personalized movie recommendations
- Modern Netflix-inspired interface

### 👤 User Authentication
- **Registration and login** system
- **Personalized experiences** for authenticated users
- **Secure chatbot access** with user-specific recommendations

---

## 🎨 Design & UI Improvements

- 🎨 **Colors:** Modern dark theme with red accents (#e50914)
- 🔤 **Typography:** Roboto font family for better readability
- 📦 **UI Components:** Enhanced cards, overlays, and interactive elements
- ✨ **Animations:** Smooth hover effects and page transitions
- 📱 **Responsive:** Mobile-first and touch-optimized design
- 🔧 **Error Handling:** Graceful JavaScript error management
- 🎯 **Navigation:** Improved menu structure and user flow

---

## 🔧 Recent Improvements & Bug Fixes

### ✅ Authentication System
- Implemented Django user authentication
- Conditional chatbot access based on login status
- Personalized user experiences

### 🗺️ Map Integration
- Enhanced Leaflet.js integration across all pages
- Interactive markers for destinations, restaurants, and hotels
- Responsive map design

### 🤖 Chatbot Enhancements
- Improved error handling for API calls
- Graceful fallback when chatbot elements are missing
- Authentication-based access control

### 🎨 UI/UX Improvements
- Consistent design language across all pages
- Enhanced footer with proper spacing
- Improved navigation menu structure
- Better responsive design

### 🐛 Bug Fixes
- Fixed JavaScript errors when chatbot elements are not present
- Resolved navigation menu routing issues
- Improved default recommendation display for non-authenticated users
- Enhanced error handling for API failures

---

## 📋 Current Status

### ✅ Completed Features
- Full user authentication system
- Interactive maps for all recommendation types
- AI chatbots with Gemini integration
- Qloo API integration for recommendations
- Responsive design across all devices
- Default recommendations for all users
- Enhanced error handling and user experience

### 🚧 In Progress
- Advanced user preference management
- Booking system integration
- Enhanced recommendation algorithms

### 📅 Future Vision
- Native mobile app development
- Real-time booking integrations
- Advanced AI personalization
- Social features and user reviews

---

## 🤝 Contributing

We welcome contributions from everyone!

```bash
# Contributing steps
- Fork this repository
- Create a new branch (feature/my-feature)
- Commit your changes
- Push the branch
- Open a Pull Request
```

### 📌 Guidelines
- Follow [PEP8](https://peps.python.org/pep-0008/) coding style  
- Write clear, descriptive commit messages  
- Include unit tests for new features
- Ensure responsive design compatibility
- Test authentication flows

---

## 📄 Dependencies

- **Django 4.2+** – Web framework with authentication
- **Requests** – API calls to external services
- **Pillow** – Image processing capabilities
- **Leaflet.js** – Interactive maps
- **Font Awesome** – Icon library
- **Google Fonts (Roboto)** – Typography

---

## 🏆 Acknowledgments

- **Qloo** – Cultural AI recommendation engine
- **Gemini (Google)** – Conversational AI platform
- **Unsplash** – High-quality image provider
- **Django** – Robust backend framework
- **Leaflet** – Open-source mapping library
- **Open Source Community** – Tools & support

---

## 📞 Contact

- 📧 Email: [contact@culturo.com](sorolj@ept.sn)  
- 🐙 GitHub: [Culturo Repository](https://github.com/kingWD123/Culturo)  
- [demo](https://youtu.be/KOBKu__Sg1E)
- 📚 Documentation: Project Wiki

---

**Culturo – Transform your passion into a cultural passport 🌍✨**

Developed with ❤️ to revolutionize global cultural discovery through intelligent AI recommendations and immersive user experiences.
