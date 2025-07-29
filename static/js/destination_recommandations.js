document.addEventListener('DOMContentLoaded', function () {
    // Map Initialization
    const map = L.map('map').setView([48.85, 2.35], 5); // Default view
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);
    let markers = [];

    // Function to update the map with new destinations
    function updateMap(destinations) {
        // Clear existing markers
        markers.forEach(marker => map.removeLayer(marker));
        markers = [];

        if (!destinations || destinations.length === 0) return;

        destinations.forEach(dest => {
            const locationString = `${dest.location1 || ''}${dest.location2 ? ', ' + dest.location2 : ''}`;
            const marker = L.marker([dest.latitude, dest.longitude]).addTo(map);
            marker.bindPopup(`
                <div style='min-width:180px; font-family: sans-serif;'>
                    <img src='${dest.img}' alt='Image of ${dest.name}' style='width:100%;height:90px;object-fit:cover;border-radius:0.5rem;margin-bottom:0.5rem;'>
                    <b style='font-size:1.1em;'>${dest.name}</b><br>
                    <span style='color:#4a5568;font-size:0.9em;'>${locationString}</span>
                </div>
            `);
            markers.push(marker);
        });

        // Center map on the first result
        map.setView([destinations[0].latitude, destinations[0].longitude], 8);
    }

    // Function to update the carousel with new destinations
    function updateCarousel(destinations) {
        const carouselTrack = document.getElementById('carouselTrack');
        if (!destinations || destinations.length === 0) {
            carouselTrack.innerHTML = "<p style='color:white;opacity:0.7;padding:1rem;'>No destinations found at the moment.</p>";
            return;
        }

        carouselTrack.innerHTML = destinations.map(d => {
            const locationString = `${d.location1 || ''}${d.location2 ? ', ' + d.location2 : ''}`;
            return `
            <div class="carousel-card" onclick="window.location.href='/destination/detail/${encodeURIComponent(d.name)}/'">
                <img src="${d.img}" alt="Image of ${d.name}">
                <h3>${d.name}</h3>
                <p>${locationString}</p>
                <div class="booking-hint">
                    Click to view details and book
                </div>
            </div>
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

    // Chatbot Logic
    const toggle = document.getElementById('chatbot-toggle');
    const chatbot = document.getElementById('destination-chatbot');
    const closeBtnChatbot = document.getElementById('chatbot-close');
    const chatForm = document.getElementById('chatbot-form');
    const chatInput = document.getElementById('chatbot-input');
    const chatBox = document.getElementById('chatbot-messages');
    let chatHistory = [];

    // Show chatbot by default on page load
    chatbot.style.display = 'flex';

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

        // Display user message
        const userDiv = document.createElement('div');
        userDiv.className = 'chat-bubble user-message';
        userDiv.textContent = userMsg;
        chatBox.appendChild(userDiv);
        chatInput.value = '';
        chatBox.scrollTop = chatBox.scrollHeight;
        chatHistory.push({ role: 'user', content: userMsg });

        // Call destination API
        try {
            const response = await fetch("/destination/api/", {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ history: chatHistory })
            });
            const data = await response.json();
            
            console.log('API Response:', data);
            console.log('Destinations received:', data.destinations);

            // Filter out technical JSON from the response
            let botMsg = data.message;
            botMsg = botMsg.replace(/```json[\s\S]*?```/gi, '');

            // Always display the conversational bot response
            if (botMsg.trim()) {
                const botDiv = document.createElement('div');
                botDiv.className = 'chat-bubble bot-message';
                botDiv.textContent = botMsg.trim();
                chatBox.appendChild(botDiv);
                chatBox.scrollTop = chatBox.scrollHeight;
            }
            chatHistory.push({ role: 'model', content: data.message });

            // Display recommendations only if they exist
            if (data.destinations && data.destinations.length > 0) {
                console.log('Updating map and carousel with destinations:', data.destinations);
                updateMap(data.destinations);
                updateCarousel(data.destinations);
                
                // Make carousel visible if it's hidden
                if (carouselContainer.classList.contains('hidden')) {
                    carouselContainer.classList.remove('hidden');
                    showCarouselBtn.classList.remove('visible');
                }
            } else {
                console.log('No destinations received in response');
            }
        } catch (error) {
            console.error('Error during chatbot interaction:', error);
            const errorDiv = document.createElement('div');
            errorDiv.className = 'chat-bubble bot-message';
            errorDiv.textContent = 'Sorry, an error occurred. Please try again.';
            chatBox.appendChild(errorDiv);
            chatBox.scrollTop = chatBox.scrollHeight;
        }
    });

    // --- Initial Load ---
    async function fetchInitialDestinations() {
        // Generate default destinations directly
        const defaultDestinations = [
            {
                name: "Paris",
                location1: "France",
                location2: "Europe",
                latitude: 48.8566,
                longitude: 2.3522,
                img: "https://images.unsplash.com/photo-1549144511-f099e773c147?w=400&h=300&fit=crop"
            },
            {
                name: "Tokyo",
                location1: "Japan",
                location2: "Asia",
                latitude: 35.6762,
                longitude: 139.6503,
                img: "https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?w=400&h=300&fit=crop"
            },
            {
                name: "New York",
                location1: "United States",
                location2: "North America",
                latitude: 40.7128,
                longitude: -74.0060,
                img: "https://images.unsplash.com/photo-1496442226666-8d4d0e62e6e9?w=400&h=300&fit=crop"
            },
            {
                name: "Rome",
                location1: "Italy",
                location2: "Europe",
                latitude: 41.9028,
                longitude: 12.4964,
                img: "https://images.unsplash.com/photo-1552832230-c0197dd311b5?w=400&h=300&fit=crop"
            },
            {
                name: "Barcelona",
                location1: "Spain",
                location2: "Europe",
                latitude: 41.3851,
                longitude: 2.1734,
                img: "https://images.unsplash.com/photo-1539037116277-4db20889f2d4?w=400&h=300&fit=crop"
            },
            {
                name: "Bali",
                location1: "Indonesia",
                location2: "Asia",
                latitude: -8.3405,
                longitude: 115.0920,
                img: "https://images.unsplash.com/photo-1537953773345-d172ccf13cf1?w=400&h=300&fit=crop"
            }
        ];

        // Update map and carousel with default destinations
        updateMap(defaultDestinations);
        updateCarousel(defaultDestinations);
        
        console.log('Default destinations loaded:', defaultDestinations);
    }

    // Launch automatic retrieval on page load
    fetchInitialDestinations();
});