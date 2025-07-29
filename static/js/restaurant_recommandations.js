document.addEventListener('DOMContentLoaded', function () {
    // Map Initialization
    const map = L.map('map').setView([48.85, 2.35], 5); // Default view
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);
    let markers = [];

    // Function to update the map with new restaurants
    function updateMap(restaurants) {
        // Clear existing markers
        markers.forEach(marker => map.removeLayer(marker));
        markers = [];

        if (!restaurants || restaurants.length === 0) return;

        restaurants.forEach(rest => {
            const marker = L.marker([rest.latitude, rest.longitude]).addTo(map);
            marker.bindPopup(`
                <div style='min-width:180px; font-family: sans-serif;'>
                    <img src='${rest.img}' alt='Image de ${rest.name}' style='width:100%;height:90px;object-fit:cover;border-radius:0.5rem;margin-bottom:0.5rem;'>
                    <b style='font-size:1.1em;'>${rest.name}</b><br>
                    <span style='color:#4a5568;font-size:0.9em;'>${rest.cuisine} - ${rest.location}</span><br>
                    <span style='color:#4a5568;font-size:0.9em;'>Prix: ${rest.price_range} - Note: ${rest.rating}</span>
                </div>
            `);
            markers.push(marker);
        });

        // Center map on the first result
        map.setView([restaurants[0].latitude, restaurants[0].longitude], 12);
    }

    // Function to update the carousel with new restaurants
    function updateCarousel(restaurants) {
        const carouselTrack = document.getElementById('carouselTrack');
        if (!restaurants || restaurants.length === 0) {
            carouselTrack.innerHTML = "<p style='color:white;opacity:0.7;padding:1rem;'>No restaurants found at the moment.</p>";
            return;
        }

        carouselTrack.innerHTML = restaurants.map(r => {
            return `
            <a href="/restaurants/detail/${encodeURIComponent(r.name)}/" class="carousel-card-link">
                <div class="carousel-card">
                    <img src="${r.img}" alt="Image of ${r.name}">
                    <h3>${r.name}</h3>
                    <p>${r.cuisine} - ${r.location}</p>
                    <div class="price">${r.price_range} - Rating: ${r.rating}</div>
                    <div class="booking-hint">
                        Click to view details and book
                    </div>
                </div>
            </a>
        `}).join('');
    }

    // Sidebar logic
    const sidebar = document.getElementById('sidebarFloat');
    const openSidebarBtn = document.getElementById('openSidebarBtn');
    const closeSidebarBtn = document.getElementById('closeSidebarBtn');

    openSidebarBtn.addEventListener('click', () => sidebar.classList.add('open'));
    closeSidebarBtn.addEventListener('click', () => sidebar.classList.remove('open'));

    // Carousel hide/show logic
    const carouselContainer = document.getElementById('bottomCarousel');
    const showCarouselBtn = document.getElementById('showCarouselBtn');
    const hideCarouselBtn = document.getElementById('hideCarouselBtn');

    carouselContainer.classList.add('carousel-entry'); // Initial animation
    hideCarouselBtn.addEventListener('click', () => {
        carouselContainer.classList.add('hidden');
        showCarouselBtn.classList.add('visible');
    });

    showCarouselBtn.addEventListener('click', () => {
        carouselContainer.classList.remove('hidden');
        showCarouselBtn.classList.remove('visible');
    });

    // Helper function to get CSRF token
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Chatbot Logic
    const toggle = document.getElementById('chatbot-toggle');
    const chatbot = document.getElementById('restaurant-chatbot');
    const closeBtnChatbot = document.getElementById('chatbot-close');
    const chatForm = document.getElementById('chatbot-form');
    const chatInput = document.getElementById('chatbot-input');
    const chatBox = document.getElementById('chatbot-messages');
    
    // Initialize chat history with welcome message
    const welcomeMessage = document.querySelector('.chat-bubble.bot-message').textContent.trim();
    let chatHistory = [
        { role: 'model', content: welcomeMessage }
    ];
    
    console.log('Initial chat history:', chatHistory);

    toggle.addEventListener('click', () => {
        chatbot.style.display = chatbot.style.display === 'none' || chatbot.style.display === '' ? 'flex' : 'none';
    });

    closeBtnChatbot.addEventListener('click', () => {
        chatbot.style.display = 'none';
    });

    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const userMsg = chatInput.value.trim();
        if (!userMsg) return;

        try {
            console.log('Sending user message:', userMsg);
            console.log('Current conversation history:', JSON.stringify(chatHistory));
            
            // Display user message
            const userDiv = document.createElement('div');
            userDiv.className = 'chat-bubble user-message';
            userDiv.textContent = userMsg;
            chatBox.appendChild(userDiv);
            chatInput.value = '';
            chatBox.scrollTop = chatBox.scrollHeight;
            chatHistory.push({ role: 'user', content: userMsg });

            // Call restaurant API with correct URL
            console.log('Calling restaurant API...');
            const response = await fetch("/restaurants/api/chatbot/", {
                method: 'POST',
                headers: { 
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({ history: chatHistory })
            });
            
            if (!response.ok) {
                throw new Error(`HTTP Error: ${response.status}`);
            }
            
            const data = await response.json();
            console.log('API response:', data);

            // Filter technical JSON from response
            let botMsg = data.message;
            botMsg = botMsg.replace(/```json[\s\S]*?```/gi, '');
            console.log('Filtered bot message:', botMsg);

            // Always display conversational bot response
            if (botMsg && botMsg.trim()) {
                const botDiv = document.createElement('div');
                botDiv.className = 'chat-bubble bot-message';
                botDiv.textContent = botMsg.trim();
                chatBox.appendChild(botDiv);
                chatBox.scrollTop = chatBox.scrollHeight;
            } else {
                console.warn('Empty bot message after filtering');
            }
            
            chatHistory.push({ role: 'model', content: data.message });

            // Display recommendations only if they exist
            if (data.restaurants && data.restaurants.length > 0) {
                console.log('Updating map and carousel with', data.restaurants.length, 'restaurants');
                updateMap(data.restaurants);
                updateCarousel(data.restaurants);
                // Make carousel visible if it's not already
                carouselContainer.classList.remove('hidden');
                showCarouselBtn.classList.remove('visible');
            } else {
                console.warn('No restaurants received in response');
            }
        } catch (error) {
            console.error('Error during chatbot interaction:', error);
            const errorDiv = document.createElement('div');
            errorDiv.className = 'chat-bubble bot-message error';
            errorDiv.textContent = 'Sorry, an error occurred. Please try again.';
            chatBox.appendChild(errorDiv);
            chatBox.scrollTop = chatBox.scrollHeight;
        }
    });

    // --- Initial Load ---
    async function fetchInitialRestaurants() {
        // Display loading state
        document.getElementById('carouselTrack').innerHTML = "<p style='color:white;opacity:0.7;padding:1rem;'>Chargement des recommandations...</p>";

        try {
            console.log('Generating initial restaurant recommendations...');
            
            // Générer des recommandations par défaut directement
            const defaultRestaurants = [
                {
                    name: "Le Petit Bistrot",
                    cuisine: "French",
                    location: "Paris, France",
                    price_range: "€€€",
                    rating: 4.5,
                    description: "Un charmant bistrot français au cœur de Paris.",
                    latitude: 48.8566 + Math.random() * 0.1 - 0.05,
                    longitude: 2.3522 + Math.random() * 0.1 - 0.05,
                    img: "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?q=80&w=1000&auto=format&fit=crop"
                },
                {
                    name: "Sakura Sushi",
                    cuisine: "Japanese",
                    location: "Tokyo, Japan",
                    price_range: "€€",
                    rating: 4.7,
                    description: "Sushi authentique dans un cadre traditionnel japonais.",
                    latitude: 35.6762 + Math.random() * 0.1 - 0.05,
                    longitude: 139.6503 + Math.random() * 0.1 - 0.05,
                    img: "https://images.unsplash.com/photo-1579584425555-c3ce17fd4351?q=80&w=1000&auto=format&fit=crop"
                },
                {
                    name: "Bella Vista",
                    cuisine: "Italian",
                    location: "Rome, Italy",
                    price_range: "€€",
                    rating: 4.3,
                    description: "Cuisine italienne traditionnelle avec vue sur la ville éternelle.",
                    latitude: 41.9028 + Math.random() * 0.1 - 0.05,
                    longitude: 12.4964 + Math.random() * 0.1 - 0.05,
                    img: "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?q=80&w=1000&auto=format&fit=crop"
                },
                {
                    name: "Spice Garden",
                    cuisine: "Indian",
                    location: "London, UK",
                    price_range: "€€",
                    rating: 4.4,
                    description: "Saveurs authentiques de l'Inde dans le cœur de Londres.",
                    latitude: 51.5074 + Math.random() * 0.1 - 0.05,
                    longitude: -0.1278 + Math.random() * 0.1 - 0.05,
                    img: "https://images.unsplash.com/photo-1565557623262-b51c2513a641?q=80&w=1000&auto=format&fit=crop"
                },
                {
                    name: "El Corazón",
                    cuisine: "Mexican",
                    location: "Barcelona, Spain",
                    price_range: "€€",
                    rating: 4.2,
                    description: "Cuisine mexicaine vibrante dans l'atmosphère catalane.",
                    latitude: 41.3851 + Math.random() * 0.1 - 0.05,
                    longitude: 2.1734 + Math.random() * 0.1 - 0.05,
                    img: "https://images.unsplash.com/photo-1565299507177-b0ac66763828?q=80&w=1000&auto=format&fit=crop"
                },
                {
                    name: "Golden Dragon",
                    cuisine: "Chinese",
                    location: "New York, USA",
                    price_range: "€€€",
                    rating: 4.6,
                    description: "Cuisine chinoise raffinée au cœur de Manhattan.",
                    latitude: 40.7128 + Math.random() * 0.1 - 0.05,
                    longitude: -74.0060 + Math.random() * 0.1 - 0.05,
                    img: "https://images.unsplash.com/photo-1526318896980-cf78c088247c?q=80&w=1000&auto=format&fit=crop"
                }
            ];

            console.log('Initial update of map and carousel with', defaultRestaurants.length, 'restaurants');
            updateMap(defaultRestaurants);
            updateCarousel(defaultRestaurants);
            
            // Make carousel visible
            carouselContainer.classList.remove('hidden');
            showCarouselBtn.classList.remove('visible');
            
            // Add initial bot message about the recommendations
            const initialBotMessage = "Here are some recommendations for popular restaurants around the world! Tell me which type of cuisine or city interests you for personalized suggestions.";
            
            // Update chat history
            chatHistory = [
                { role: 'model', content: welcomeMessage },
                { role: 'model', content: initialBotMessage }
            ];
            
            // Display the initial bot message
            const botDiv = document.createElement('div');
            botDiv.className = 'chat-bubble bot-message';
            botDiv.textContent = initialBotMessage;
            chatBox.appendChild(botDiv);
            chatBox.scrollTop = chatBox.scrollHeight;
            
            console.log('Chat history after initial response:', JSON.stringify(chatHistory));
            
        } catch (error) {
            console.error("Error loading initial restaurants:", error);
            document.getElementById('carouselTrack').innerHTML = "<p style='color:white;opacity:0.7;padding:1rem;'>Erreur lors du chargement des restaurants.</p>";
            
            const errorDiv = document.createElement('div');
            errorDiv.className = 'chat-bubble bot-message error';
            errorDiv.textContent = 'Désolé, une erreur s\'est produite lors du chargement des recommandations initiales. Posez-moi une question pour obtenir des recommandations.';
            chatBox.appendChild(errorDiv);
            chatBox.scrollTop = chatBox.scrollHeight;
        }
    }

    // Launch automatic fetch on page load
    fetchInitialRestaurants();
});