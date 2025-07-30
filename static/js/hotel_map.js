document.addEventListener('DOMContentLoaded', function() {
    // Initialize map
    const map = L.map('map').setView([48.8566, 2.3522], 2);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);

    // Use featureGroup instead of layerGroup to have getBounds() method
    let markersGroup = L.featureGroup().addTo(map);

    // Fallback hotel data
    const fallbackHotels = [
        {
            'name': 'The Ritz Paris',
            'location': 'Paris, France',
            'rating': '4.8',
            'price_range': '$$$$',
            'description': 'Legendary luxury hotel in the heart of Paris',
            'amenities': ['spa', 'restaurant', 'bar', 'concierge'],
            'coordinates': {'lat': 48.8566, 'lng': 2.3522},
            'img': 'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=400'
        },
        {
            'name': 'Marina Bay Sands',
            'location': 'Singapore',
            'rating': '4.7',
            'price_range': '$$$$',
            'description': 'Iconic hotel with infinity pool and stunning views',
            'amenities': ['pool', 'casino', 'shopping', 'restaurants'],
            'coordinates': {'lat': 1.2834, 'lng': 103.8607},
            'img': 'https://images.unsplash.com/photo-1540541338287-41700207dee6?w=400'
        },
        {
            'name': 'The Plaza Hotel',
            'location': 'New York, USA',
            'rating': '4.6',
            'price_range': '$$$$',
            'description': 'Historic luxury hotel overlooking Central Park',
            'amenities': ['spa', 'restaurant', 'fitness center', 'business center'],
            'coordinates': {'lat': 40.7648, 'lng': -73.9808},
            'img': 'https://images.unsplash.com/photo-1566073771259-6a8506099945?w=400'
        }
    ];

    // Get DOM elements
    const carouselContainer = document.getElementById('bottomCarousel');
    const hideCarouselBtn = document.getElementById('hideCarouselBtn');
    const showCarouselBtn = document.getElementById('showCarouselBtn');
    const carouselTrack = document.getElementById('carouselTrack');

    // Function to show carousel
    function showCarousel() {
        if (carouselContainer) {
            carouselContainer.classList.remove('hidden');
            console.log('Carousel shown');
        }
        if (showCarouselBtn) {
            showCarouselBtn.classList.remove('visible');
        }
    }

    // Function to hide carousel
    function hideCarousel() {
        if (carouselContainer) {
            carouselContainer.classList.add('hidden');
        }
        if (showCarouselBtn) {
            showCarouselBtn.classList.add('visible');
        }
    }

    // Function to update map with hotels
    function updateMap(hotels) {
        markersGroup.clearLayers();
        
        if (!hotels || hotels.length === 0) {
            console.warn('No hotels to display on map');
            return;
        }

        hotels.forEach(hotel => {
            if (hotel.coordinates && hotel.coordinates.lat && hotel.coordinates.lng) {
                const marker = L.marker([hotel.coordinates.lat, hotel.coordinates.lng])
                    .bindPopup(`
                        <div style="text-align: center;">
                            <h3>${hotel.name}</h3>
                            <p><strong>Location:</strong> ${hotel.location}</p>
                            <p><strong>Rating:</strong> ${hotel.rating} ⭐</p>
                            <p><strong>Price:</strong> ${hotel.price_range}</p>
                        </div>
                    `);
                markersGroup.addLayer(marker);
            }
        });

        // Fit map to show all markers - now this will work correctly
        if (markersGroup.getLayers().length > 0) {
            try {
                map.fitBounds(markersGroup.getBounds(), { padding: [20, 20] });
                console.log('Map bounds updated successfully');
            } catch (error) {
                console.error('Error fitting map bounds:', error);
                // Fallback to default view if bounds fail
                map.setView([48.8566, 2.3522], 2);
            }
        }
    }

    // Function to update carousel with hotels
    function updateCarousel(hotels) {
        if (!carouselTrack) {
            console.error('Carousel track not found');
            return;
        }
        
        if (!hotels || hotels.length === 0) {
            carouselTrack.innerHTML = "<p style='color:white;opacity:0.7;padding:1rem;'>No hotels found. Try asking for recommendations!</p>";
            return;
        }

        carouselTrack.innerHTML = '';
        
        hotels.forEach(hotel => {
            const card = document.createElement('div');
            card.className = 'carousel-card';
            
            // Add click handler to navigate to hotel detail page
            card.onclick = () => {
                window.location.href = `/hotels/detail/${encodeURIComponent(hotel.name)}/`;
            };
            
            // Add cursor pointer style
            card.style.cursor = 'pointer';
            
            // Use fallback image if none provided
            const imageUrl = hotel.img || 'https://images.unsplash.com/photo-1566073771259-6a8506099945?w=400';
            
            card.innerHTML = `
                <img src="${imageUrl}" alt="${hotel.name}" onerror="this.src='https://images.unsplash.com/photo-1566073771259-6a8506099945?w=400'">
                <div class="card-content">
                    <h3>${hotel.name}</h3>
                    <p class="location">${hotel.location}</p>
                    <p class="description">${hotel.description}</p>
                    <div class="amenities">
                        ${hotel.amenities ? hotel.amenities.slice(0, 3).map(amenity => `<span class="amenity">${amenity}</span>`).join('') : ''}
                    </div>
                    <div class="card-footer">
                        <span class="rating">${hotel.rating} ⭐</span>
                        <span class="price">${hotel.price_range}</span>
                    </div>
                    <div class="booking-hint">
                        Click to view details and book
                    </div>
                </div>
            `;
            carouselTrack.appendChild(card);
        });

        // Show carousel after updating
        showCarousel();
        console.log('Carousel updated with', hotels.length, 'hotels');
    }

    // Sidebar functionality
    const openSidebarBtn = document.getElementById('openSidebarBtn');
    const closeSidebarBtn = document.getElementById('closeSidebarBtn');
    const sidebar = document.getElementById('sidebarFloat');

    if (openSidebarBtn && closeSidebarBtn && sidebar) {
        openSidebarBtn.addEventListener('click', () => {
            sidebar.classList.add('visible');
        });

        closeSidebarBtn.addEventListener('click', () => {
            sidebar.classList.remove('visible');
        });
    }

    // Carousel visibility controls
    if (hideCarouselBtn && showCarouselBtn) {
        hideCarouselBtn.addEventListener('click', hideCarousel);
        showCarouselBtn.addEventListener('click', showCarousel);
    }

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
    const chatbot = document.getElementById('hotel-chatbot');
    const closeBtnChatbot = document.getElementById('chatbot-close');
    const chatForm = document.getElementById('chatbot-form');
    const chatInput = document.getElementById('chatbot-input');
    const chatBox = document.getElementById('chatbot-messages');
    
    // Initialize chat history with welcome message only if chatbot elements exist
    const welcomeMessageElement = document.querySelector('.chat-bubble.bot-message');
    const welcomeMessage = welcomeMessageElement ? welcomeMessageElement.textContent.trim() : "Hello! I'm your hotel assistant.";
    let chatHistory = [
        { role: 'model', content: welcomeMessage }
    ];
    
    console.log('Initial chat history:', chatHistory);

    // Chatbot toggle functionality - only if elements exist
    if (toggle && chatbot) {
        toggle.addEventListener('click', () => {
            if (chatbot.style.display === 'none') {
                chatbot.style.display = 'flex';
            } else {
                chatbot.style.display = 'none';
            }
        });
    }

    if (closeBtnChatbot && chatbot) {
        closeBtnChatbot.addEventListener('click', () => {
            chatbot.style.display = 'none';
        });
    }

    // Chatbot form submission - only if all required elements exist
    if (chatForm && chatInput && chatBox) {
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

                // Call hotel API with correct URL
                console.log('Calling hotel API...');
                const response = await fetch("/hotels/api/chatbot/", {
                    method: 'POST',
                    headers: { 
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken')
                    },
                    body: JSON.stringify({ history: chatHistory })
                });
                
                console.log('Response status:', response.status);
                
                if (!response.ok) {
                    const errorText = await response.text();
                    console.error('API Error Response:', errorText);
                    throw new Error(`HTTP Error: ${response.status} - ${errorText}`);
                }
                
                const data = await response.json();
                console.log('API response:', data);

                // Filter technical JSON from response
                let botMsg = data.message || 'Sorry, I received an empty response.';
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
                
                chatHistory.push({ role: 'model', content: data.message || botMsg });

                // Display recommendations only if they exist
                if (data.hotels && data.hotels.length > 0) {
                    console.log('Updating map and carousel with', data.hotels.length, 'hotels');
                    updateMap(data.hotels);
                    updateCarousel(data.hotels);
                } else {
                    console.warn('No hotels received in response');
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
    }

    // --- Initial Load ---
    async function fetchInitialHotels() {
        // Display loading state
        if (carouselTrack) {
            carouselTrack.innerHTML = "<p style='color:white;opacity:0.7;padding:1rem;'>Searching for hotel recommendations...</p>";
        }

        // Show carousel immediately with loading message
        showCarousel();

        // Use simple initial history
        const initialHistory = [{ role: 'user', content: 'Give me popular hotel recommendations worldwide.' }];
        console.log('Initial history for request:', JSON.stringify(initialHistory));

        try {
            console.log('Initial call to hotel API...');
            const response = await fetch("/hotels/api/chatbot/", {
                method: 'POST',
                headers: { 
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({ history: initialHistory })
            });
            
            console.log('Initial response status:', response.status);
            
            if (!response.ok) {
                const errorText = await response.text();
                console.warn(`API returned ${response.status}: ${errorText}, using fallback data`);
                throw new Error(`HTTP Error: ${response.status}`);
            }
            
            const data = await response.json();
            console.log('Initial API response:', data);

            if (data.hotels && data.hotels.length > 0) {
                console.log('Initial update of map and carousel with', data.hotels.length, 'hotels');
                updateMap(data.hotels);
                updateCarousel(data.hotels);
                
                // Update chat history with initial conversation only if chatbox exists
                if (chatBox) {
                    chatHistory = [
                        { role: 'model', content: welcomeMessage },
                        { role: 'user', content: initialHistory[0].content },
                        { role: 'model', content: data.message }
                    ];
                    console.log('Chat history after initial response:', JSON.stringify(chatHistory));
                    
                    // Display bot response
                    let botMsg = data.message;
                    botMsg = botMsg.replace(/```json[\s\S]*?```/gi, '');
                    
                    if (botMsg && botMsg.trim()) {
                        const botDiv = document.createElement('div');
                        botDiv.className = 'chat-bubble bot-message';
                        botDiv.textContent = botMsg.trim();
                        chatBox.appendChild(botDiv);
                        chatBox.scrollTop = chatBox.scrollHeight;
                    }
                }
            } else {
                console.warn('No hotels received in initial response, using fallback data');
                throw new Error('No hotels in API response');
            }
        } catch (error) {
            console.error("Error loading initial hotels:", error);
            console.log('Using fallback hotel data');
            
            // Use fallback data
            updateMap(fallbackHotels);
            updateCarousel(fallbackHotels);
            
            // Add a friendly message instead of error only if chatbox exists
            if (chatBox) {
                const botDiv = document.createElement('div');
                botDiv.className = 'chat-bubble bot-message';
                botDiv.textContent = 'Here are some popular hotel destinations worldwide! I can help you find more specific recommendations based on your preferences. Where would you like to stay?';
                chatBox.appendChild(botDiv);
                chatBox.scrollTop = chatBox.scrollHeight;
                
                // Update chat history
                chatHistory = [
                    { role: 'model', content: welcomeMessage },
                    { role: 'model', content: 'Here are some popular hotel destinations worldwide! I can help you find more specific recommendations based on your preferences. Where would you like to stay?' }
                ];
            }
        }
    }

    // Launch automatic fetch on page load
    fetchInitialHotels();
});