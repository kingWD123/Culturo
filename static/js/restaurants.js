document.addEventListener('DOMContentLoaded', function() {
    // Initialisation de la carte Leaflet
    let map = L.map('map').setView([46.603354, 1.888334], 6); // Vue par défaut sur la France
    let markers = [];
    
    // Ajout de la couche de tuiles OpenStreetMap
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);
    
    // Éléments du DOM
    const chatMessages = document.getElementById('chat-messages');
    const chatInput = document.getElementById('chatbot-input');
    const sendBtn = document.getElementById('send-btn');
    const sidebar = document.getElementById('sidebarFloat');
    const openSidebarBtn = document.getElementById('openSidebarBtn');
    const closeSidebarBtn = document.getElementById('closeSidebarBtn');
    const restaurantsCarousel = document.getElementById('restaurantsCarousel');
    const restaurantsTrack = document.getElementById('restaurantsTrack');
    const hideCarouselBtn = document.getElementById('hideCarouselBtn');
    const showCarouselBtn = document.getElementById('showCarouselBtn');
    const restaurantDetail = document.getElementById('restaurantDetail');
    const closeRestaurantDetail = document.getElementById('closeRestaurantDetail');
    
    // Historique de la conversation
    let conversationHistory = [];
    let currentRestaurants = [];
    
    // Fonction pour ajouter un message à la conversation
    function addMessage(role, content) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${role}-message`;
        messageDiv.innerHTML = content;
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
        
        // Ajouter à l'historique
        conversationHistory.push({ role, content });
    }
    
    // Fonction pour afficher l'indicateur de frappe
    function showTypingIndicator() {
        const typingDiv = document.createElement('div');
        typingDiv.className = 'message bot-message typing-indicator';
        typingDiv.id = 'typingIndicator';
        typingDiv.innerHTML = '<span></span><span></span><span></span>';
        chatMessages.appendChild(typingDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    // Fonction pour masquer l'indicateur de frappe
    function hideTypingIndicator() {
        const typingIndicator = document.getElementById('typingIndicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }
    }
    
    // Fonction pour envoyer un message
    async function sendMessage() {
        const message = chatInput.value.trim();
        if (!message) return;
        
        // Ajouter le message de l'utilisateur
        addMessage('user', message);
        chatInput.value = '';
        
        // Afficher l'indicateur de frappe
        showTypingIndicator();
        
        try {
            const response = await fetch('/restaurants/chatbot-api/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({
                    message: message,
                    history: conversationHistory.map(msg => ({
                        role: msg.role,
                        content: msg.content
                    }))
                })
            });
            
            const data = await response.json();
            
            // Masquer l'indicateur de frappe
            hideTypingIndicator();
            
            // Ajouter la réponse du bot
            if (data.message) {
                addMessage('bot', data.message);
            }
            
            // Mettre à jour la carte et le carrousel avec les restaurants
            if (data.restaurants && data.restaurants.length > 0) {
                currentRestaurants = data.restaurants;
                updateMap(data.restaurants);
                updateCarousel(data.restaurants);
            }
            
        } catch (error) {
            console.error('Error:', error);
            hideTypingIndicator();
            addMessage('bot', 'Sorry, something went wrong. Please try again.');
        }
    }
    
    // Fonction pour mettre à jour la carte avec les restaurants
    function updateMap(restaurants) {
        // Supprimer les marqueurs existants
        markers.forEach(marker => map.removeLayer(marker));
        markers = [];
        
        // Ajouter les nouveaux marqueurs
        if (restaurants.length === 0) return;
        
        const bounds = [];
        
        restaurants.forEach((restaurant, index) => {
            if (restaurant.latitude && restaurant.longitude) {
                const marker = L.marker([restaurant.latitude, restaurant.longitude], {
                    title: restaurant.name
                }).addTo(map);
                
                // Ajouter un popup avec les informations du restaurant
                marker.bindPopup(`
                    <div style="max-width: 200px;">
                        <h3 style="margin: 0 0 5px 0; font-size: 1em;">${restaurant.name}</h3>
                        ${restaurant.rating ? `<div>${getStarRating(restaurant.rating)}</div>` : ''}
                        <button onclick="showRestaurantDetail(${index})" style="margin-top: 5px; background: #4CAF50; color: white; border: none; padding: 5px 10px; border-radius: 4px; cursor: pointer;">
                            View Details
                        </button>
                    </div>
                `);
                
                markers.push(marker);
                bounds.push([restaurant.latitude, restaurant.longitude]);
                
                // Centrer la carte sur le premier restaurant
                if (index === 0) {
                    map.setView([restaurant.latitude, restaurant.longitude], 13);
                }
            }
        });
        
        // Ajuster la vue pour afficher tous les marqueurs s'il y en a plusieurs
        if (bounds.length > 1) {
            map.fitBounds(bounds);
        }
    }
    
    // Fonction pour mettre à jour le carrousel avec les restaurants
    function updateCarousel(restaurants) {
        // Vider le carrousel existant
        restaurantsTrack.innerHTML = '';
        
        if (restaurants.length === 0) {
            restaurantsCarousel.classList.remove('visible');
            return;
        }
        
        // Ajouter chaque restaurant au carrousel
        restaurants.forEach((restaurant, index) => {
            const card = document.createElement('div');
            card.className = 'carousel-card';
            card.dataset.index = index;
            
            // Créer l'image du restaurant
            const imageUrl = restaurant.images && restaurant.images.length > 0 
                ? restaurant.images[0] 
                : 'https://via.placeholder.com/300x200?text=No+Image';
            
            // Créer le contenu de la carte
            card.innerHTML = `
                <img src="${imageUrl}" alt="${restaurant.name}" class="carousel-card-image">
                <div class="carousel-card-content">
                    <h3>${restaurant.name}</h3>
                    ${restaurant.cuisines && restaurant.cuisines.length > 0 ? 
                        `<p><i class="fas fa-utensils"></i> ${restaurant.cuisines.join(', ')}</p>` : ''}
                    ${restaurant.rating ? 
                        `<div class="restaurant-rating">
                            ${getStarRating(restaurant.rating)}
                            <span class="rating-value">${restaurant.rating.toFixed(1)}</span>
                        </div>` : ''}
                    ${restaurant.price_level ? 
                        `<p class="price-level">${'$'.repeat(restaurant.price_level)}</p>` : ''}
                    <button class="discover-btn" onclick="showRestaurantDetail(${index})">Discover</button>
                </div>
            `;
            
            // Ajouter un gestionnaire d'événements pour afficher les détails
            card.addEventListener('click', () => showRestaurantDetail(index));
            
            restaurantsTrack.appendChild(card);
        });
        
        // Afficher le carrousel
        restaurantsCarousel.classList.add('visible');
        showCarouselBtn.classList.remove('visible');
    }
    
    // Fonction pour afficher les détails d'un restaurant
    window.showRestaurantDetail = function(index) {
        if (index < 0 || index >= currentRestaurants.length) return;
        
        const restaurant = currentRestaurants[index];
        const detailImage = document.getElementById('detailImage');
        const detailName = document.getElementById('detailName');
        const detailRating = document.getElementById('detailRating');
        const detailPrice = document.getElementById('detailPrice');
        const detailAddress = document.getElementById('detailAddress');
        const detailPhone = document.getElementById('detailPhone');
        const detailWebsite = document.getElementById('detailWebsite');
        const detailCuisines = document.getElementById('detailCuisines');
        const detailHours = document.getElementById('detailHours');
        
        // Mettre à jour l'image
        detailImage.src = restaurant.images && restaurant.images.length > 0 
            ? restaurant.images[0] 
            : 'https://via.placeholder.com/800x400?text=No+Image';
        
        // Mettre à jour le nom
        detailName.textContent = restaurant.name;
        
        // Mettre à jour la note
        if (restaurant.rating) {
            detailRating.innerHTML = `
                <span class="rating-stars">${getStarRating(restaurant.rating, '1.2rem')}</span>
                <span class="rating-value">${restaurant.rating.toFixed(1)}</span>
            `;
            detailRating.style.display = 'flex';
        } else {
            detailRating.style.display = 'none';
        }
        
        // Mettre à jour le prix
        if (restaurant.price_level) {
            detailPrice.textContent = '• ' + '$'.repeat(restaurant.price_level);
            detailPrice.style.display = 'block';
        } else {
            detailPrice.style.display = 'none';
        }
        
        // Mettre à jour l'adresse
        detailAddress.textContent = restaurant.address || 'Address not available';
        
        // Mettre à jour le téléphone
        if (restaurant.phone) {
            detailPhone.textContent = restaurant.phone;
            detailPhone.closest('.restaurant-phone').style.display = 'flex';
        } else {
            detailPhone.closest('.restaurant-phone').style.display = 'none';
        }
        
        // Mettre à jour le site web
        if (restaurant.website) {
            detailWebsite.href = restaurant.website;
            detailWebsite.textContent = new URL(restaurant.website).hostname.replace('www.', '');
            detailWebsite.closest('.restaurant-website').style.display = 'flex';
        } else {
            detailWebsite.closest('.restaurant-website').style.display = 'none';
        }
        
        // Mettre à jour les cuisines
        detailCuisines.innerHTML = '';
        if (restaurant.cuisines && restaurant.cuisines.length > 0) {
            restaurant.cuisines.forEach(cuisine => {
                const tag = document.createElement('span');
                tag.className = 'cuisine-tag-large';
                tag.textContent = cuisine;
                detailCuisines.appendChild(tag);
            });
        }
        
        // Mettre à jour les horaires d'ouverture
        detailHours.innerHTML = '';
        if (restaurant.opening_hours && restaurant.opening_hours.length > 0) {
            const days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
            const today = new Date().getDay(); // 0 = Sunday, 1 = Monday, etc.
            
            days.forEach((day, index) => {
                const row = document.createElement('tr');
                const dayCell = document.createElement('td');
                const timeCell = document.createElement('td');
                
                dayCell.textContent = day;
                
                const hours = restaurant.opening_hours.find(h => h.day === index);
                if (hours) {
                    timeCell.textContent = `${hours.open} - ${hours.close}`;
                    timeCell.className = index === today ? 'open' : '';
                } else {
                    timeCell.textContent = 'Closed';
                    timeCell.className = 'closed';
                }
                
                row.appendChild(dayCell);
                row.appendChild(timeCell);
                detailHours.appendChild(row);
            });
        } else {
            const row = document.createElement('tr');
            const cell = document.createElement('td');
            cell.colSpan = 2;
            cell.textContent = 'Opening hours not available';
            row.appendChild(cell);
            detailHours.appendChild(row);
        }
        
        // Afficher la modale
        restaurantDetail.style.display = 'flex';
        setTimeout(() => {
            restaurantDetail.classList.add('show');
        }, 10);
    };
    
    // Fonction utilitaire pour obtenir les étoiles de notation
    function getStarRating(rating, size = '0.9rem') {
        const fullStars = Math.floor(rating);
        const hasHalfStar = rating % 1 >= 0.5;
        let stars = '';
        
        for (let i = 0; i < 5; i++) {
            if (i < fullStars) {
                stars += `<i class="fas fa-star" style="color: #fbbf24; font-size: ${size};"></i>`;
            } else if (i === fullStars && hasHalfStar) {
                stars += `<i class="fas fa-star-half-alt" style="color: #fbbf24; font-size: ${size};"></i>`;
            } else {
                stars += `<i class="far fa-star" style="color: #fbbf24; font-size: ${size};"></i>`;
            }
        }
        
        return stars;
    }
    
    // Fonction utilitaire pour obtenir un cookie
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
    
    // Gestionnaires d'événements
    sendBtn.addEventListener('click', sendMessage);
    
    chatInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
    
    openSidebarBtn.addEventListener('click', function() {
        sidebar.classList.add('open');
        openSidebarBtn.classList.add('shifted');
    });
    
    closeSidebarBtn.addEventListener('click', function() {
        sidebar.classList.remove('open');
        openSidebarBtn.classList.remove('shifted');
    });
    
    hideCarouselBtn.addEventListener('click', function() {
        restaurantsCarousel.classList.remove('visible');
        showCarouselBtn.classList.add('visible');
    });
    
    showCarouselBtn.addEventListener('click', function() {
        restaurantsCarousel.classList.add('visible');
        showCarouselBtn.classList.remove('visible');
    });
    
    closeRestaurantDetail.addEventListener('click', function() {
        restaurantDetail.classList.remove('show');
        setTimeout(() => {
            restaurantDetail.style.display = 'none';
        }, 300);
    });
    
    // Fermer la modale en cliquant en dehors
    window.addEventListener('click', function(e) {
        if (e.target === restaurantDetail) {
            restaurantDetail.classList.remove('show');
            setTimeout(() => {
                restaurantDetail.style.display = 'none';
            }, 300);
        }
    });
    
    // Message de bienvenue
    addMessage('bot', 'Welcome to Restaurant Finder! 🍽️ Tell me what kind of food you\'re craving and where you are, and I\'ll help you find the perfect spot!');
});
