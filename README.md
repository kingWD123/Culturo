
# 🌍 Culturo - Intelligent Cultural Recommendations Platform

**Culturo** is an immersive web platform that **revolutionizes cultural discovery** by combining **artificial intelligence** with the **Qloo** and **Gemini APIs** to offer **personalized recommendations** for destinations, restaurants, hotels, and cinema.

---

## 🎯 Project Vision

Culturo transforms how people discover and explore global culture by offering:

- **Intelligent recommendations** based on personal tastes and preferences  
- **Interactive exploration** with maps and AI-powered chatbots  
- **Immersive experiences** through a modern, responsive UI  
- **Authentic discovery** of destinations, gastronomy, and accommodations

---

## ✨ Key Features

### 🗺️ Destination Recommendations
- AI chatbot powered by **Gemini** for personalized suggestions  
- **Qloo API** integration for taste-based recommendations  
- **Interactive maps** with dynamic markers  
- Filters by popularity, interest, and location  
- Sleek UI with cards and overlays

### 🍽️ Gastronomic Discovery
- Personalized restaurant suggestions based on user preferences  
- Geolocation support for nearby options  
- Detailed restaurant info (cuisine, price, ratings)  
- Image sourcing via **Unsplash API**

### 🏨 Quality Accommodations
- Hotel recommendations based on travel profiles  
- Support for major destinations  
- Map interface with filters by amenities and price

### 🎬 Cinema Discovery
- Taste-driven movie suggestions  
- AI chatbot focused on cinema content  
- Smooth and minimal UI

---

## 🛠️ Technical Architecture

### 🔗 Integrated APIs
- **🤖 Gemini AI** – For chatbot conversations and natural language understanding  
- **🎯 Qloo API** – Cultural and taste-based recommendation engine  
- **📸 Unsplash API** – High-quality image integration

### 🎨 Frontend Technologies
- **HTML5 / CSS3** – Responsive, mobile-first layout  
- **Vanilla JavaScript** – Dynamic interactions  
- **Leaflet.js** – Interactive maps with markers and layers  
- **Chat UI components** – For multiple chatbot interactions

### 🗂️ Data Models
```python
# User cultural profiles
CulturalProfile:
    - music, film, and food preferences
    - travel habits, budget, activity types

# Cultural destinations
Destination:
    - tags, description, cuisine, music scenes, location

# Cultural points of interest
CulturalHighlight:
    - museums, restaurants, galleries, schedules

# Personalized itineraries
Itinerary, ItineraryDay, ItineraryItem:
    - day-by-day activities with time slots and types
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

# 6. Start the development server
python manage.py runserver
```

### 🌐 Access the App
- App: [http://localhost:8000](http://localhost:8000)  
- Admin Panel: [http://localhost:8000/admin](http://localhost:8000/admin)

---

## 📱 User Guide

### 🏠 Home Page
- Immersive welcome UI with discovery sections  
- Quick access to destinations, food, and cinema

### 🌍 Destinations
- Ask the chatbot: *"I want to visit Paris"*  
- Get personalized recommendations with interactive maps

### 🍴 Restaurants
- Ask: *"Find restaurants in Tokyo"*  
- See curated suggestions with ratings and prices

### 🏨 Hotels
- Select hotels based on preference, price, and location  
- View them on the interactive map

### 🎥 Cinema
- Discover films tailored to your taste  
- Use the chatbot for cinema-based queries

---

## 🎨 Design & UI

- 🎨 **Colors:** Gradient-based modern palette  
- 🔤 **Typography:** Inter (Google Fonts)  
- 📦 **UI Components:** Cards, overlays, and image tiles  
- ✨ **Animations:** Smooth hover and page transitions  
- 📱 **Responsive:** Mobile-first and touch-optimized

---



### ✅ Current Features
- Gemini & Qloo API integrations  
- Destination, hotel, and restaurant recommendations  
- Chatbot and map components  
- Modern, responsive design

### 🚧 In Progress
- User authentication and saved preferences  
- Itinerary builder  
- Favorite places and activity history

### 📅 Future Vision
- Native mobile app  
- Booking integrations  
- Augmented reality exploration

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

---

## 📄 Dependencies

- **Django 4.2** – Web framework  
- **Requests** – API calls  
- **Pillow** – Image processing  
- **Leaflet.js** – Interactive maps  

---

## 🏆 Acknowledgments

- **Qloo** – Cultural AI  
- **Gemini (Google)** – Conversational AI  
- **Unsplash** – Image provider  
- **Django** – Backend framework  
- **Open Source Community** – Tools & support

---

## 📞 Contact

- 📧 Email: [contact@culturo.com](mailto:contact@culturo.com)  
- 🐙 GitHub: [Culturo Repository](https://github.com/kingWD123/Culturo)  
- 📚 Documentation: Project Wiki

---


**Culturo – Transform your passion into a cultural passport 🌍✨**

Developed with ❤️ to revolutionize global cultural discovery.
