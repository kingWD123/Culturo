document.addEventListener('DOMContentLoaded', function() {
    const chatContainer = document.getElementById('chat-container');
    const chatMessages = document.getElementById('chat-messages');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');
    
    // Initial bot message
    addBotMessage("Bonjour ! Je suis votre assistant de voyage. Dans quelle ville ou pays souhaitez-vous des recommandations de restaurants ?");
    
    // Send message when button is clicked
    sendButton.addEventListener('click', sendMessage);
    
    // Send message when Enter key is pressed
    userInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
    
    function sendMessage() {
        const message = userInput.value.trim();
        if (message === '') return;
        
        // Add user message to chat
        addUserMessage(message);
        userInput.value = '';
        
        // Show typing indicator
        const typingIndicator = addTypingIndicator();
        
        // Send message to backend
        fetch('/restaurants/api/chatbot/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                history: [{ role: 'user', content: message }]
            })
        })
        .then(response => response.json())
        .then(data => {
            // Remove typing indicator
            chatMessages.removeChild(typingIndicator);
            
            // Add bot's response
            if (data.message) {
                addBotMessage(data.message);
            }
            
            // Display restaurants if available
            if (data.restaurants && data.restaurants.length > 0) {
                displayRestaurants(data.restaurants);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            chatMessages.removeChild(typingIndicator);
            addBotMessage("Désolé, une erreur s'est produite. Veuillez réessayer.");
        });
    }
    
    function addUserMessage(message) {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message user-message';
        messageDiv.textContent = message;
        chatMessages.appendChild(messageDiv);
        scrollToBottom();
    }
    
    function addBotMessage(message) {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message bot-message';
        messageDiv.textContent = message;
        chatMessages.appendChild(messageDiv);
        scrollToBottom();
    }
    
    function addTypingIndicator() {
        const typingDiv = document.createElement('div');
        typingDiv.className = 'typing-indicator';
        typingDiv.innerHTML = '<span></span><span></span><span></span>';
        chatMessages.appendChild(typingDiv);
        scrollToBottom();
        return typingDiv;
    }
    
    function displayRestaurants(restaurants) {
        const container = document.createElement('div');
        container.className = 'restaurants-container';
        
        restaurants.forEach(restaurant => {
            const restaurantDiv = document.createElement('div');
            restaurantDiv.className = 'restaurant-card';
            
            let content = `
                <h3>${restaurant.name || 'Nom non disponible'}</h3>
                <p>${restaurant.location || 'Adresse non disponible'}</p>
                <p>Cuisine: ${restaurant.cuisine || 'Non spécifiée'}</p>
                <p>Note: ${restaurant.rating || 'Non noté'}/5</p>
                <p>Prix: ${restaurant.price_range || '€€'}</p>
            `;
            
            if (restaurant.img) {
                content = `<img src="${restaurant.img}" alt="${restaurant.name}" style="width:100%;height:120px;object-fit:cover;border-radius:4px;margin-bottom:8px;">` + content;
            }
            
            restaurantDiv.innerHTML = content;
            container.appendChild(restaurantDiv);
        });
        
        chatMessages.appendChild(container);
        scrollToBottom();
    }
    
    function scrollToBottom() {
        chatMessages.scrollTop = chatMessages.scrollHeight;
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
});
