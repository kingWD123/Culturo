// Cinema Recommendations JavaScript

console.log('Cinema recommendations JS loaded');

document.addEventListener('DOMContentLoaded', function() {
    console.log('=== DEBUG: Starting recommendation loading ===');
    
    // Initialize recommendations from Django template
    var initialElement = document.getElementById('initial-recommendations');
    if (!initialElement) {
        console.error('❌ ERROR: Element with ID "initial-recommendations" not found');
        return;
    }
    
    console.log('✅ Raw JSON script data:', initialElement.textContent);
    
    var recommendations = [];
    try {
        recommendations = JSON.parse(initialElement.textContent);
        console.log('✅ Data parsed successfully:', recommendations);
        
        // Display detailed information for each movie
        if (recommendations && Array.isArray(recommendations)) {
            console.log(`📊 Number of recommendations: ${recommendations.length}`);
            recommendations.forEach((film, index) => {
                console.log(`\n🎬 Movie #${index + 1}:`);
                console.log(`   Name: ${film.name || 'Not specified'}`);
                console.log(`   ID: ${film.entity_id || 'Not specified'}`);
                console.log('   Image properties:', {
                    'film.image': film.image,
                    'film.image_url': film.image_url,
                    'film.properties.image': film.properties?.image,
                    'film.properties.poster_path': film.properties?.poster_path
                });
            });
        } else {
            console.warn('⚠️ Recommendations is not an array:', recommendations);
        }
    } catch (e) {
        console.error('❌ ERROR parsing recommendations:', e);
        console.error('Raw recommendation content:', initialElement.textContent);
        return;
    }
    
    if (recommendations && Array.isArray(recommendations)) {
        console.log('Calling updateNowShowing with', recommendations.length, 'recommendations');
        updateNowShowing(recommendations);
    } else {
        console.error('Recommendations is not an array or is empty:', recommendations);
        // Display error message to user
        const grid = document.querySelector('.cinema-movies-grid');
        if (grid) {
            grid.innerHTML = '<div class="error-message">Unable to load recommendations. Please try again later.</div>';
        }
    }

    // Initialize chatbot functionality
    initializeChatbot();
});

function initializeChatbot() {
    var toggle = document.getElementById('chatbot-toggle');
    var chatbot = document.getElementById('cinema-chatbot');
    var closeBtn = document.getElementById('chatbot-close');
    
    if (toggle && chatbot) {
        toggle.addEventListener('click', function () {
            chatbot.style.display = chatbot.style.display === 'none' ? 'flex' : 'none';
        });
    }
    
    if (closeBtn && chatbot) {
        closeBtn.addEventListener('click', function () {
            chatbot.style.display = 'none';
        });
    }

    // Dynamic cinema recommendations display
    var chatbotForm = document.getElementById('chatbot-form');
    var chatbotInput = document.getElementById('chatbot-input');
    var chatbotMessages = document.getElementById('chatbot-messages');
    var recSection = document.getElementById('cinema-recommendations-section');
    var recList = document.getElementById('cinema-recommendations');
    var recLoading = document.getElementById('cinema-recommendations-loading');
    var chatHistory = [];
    
    if (chatbotForm && chatbotInput && chatbotMessages) {
        chatbotForm.addEventListener('submit', async function (e) {
            e.preventDefault();
            var userMsg = chatbotInput.value.trim();
            if (!userMsg) return;
            
            // Display user message
            var userDiv = document.createElement('div');
            userDiv.style.alignSelf = 'flex-end';
            userDiv.style.background = '#ffecd2';
            userDiv.style.borderRadius = '12px';
            userDiv.style.padding = '0.7rem 1rem';
            userDiv.style.margin = '0.2rem 0';
            userDiv.style.maxWidth = '85%';
            userDiv.textContent = userMsg;
            chatbotMessages.appendChild(userDiv);
            chatbotInput.value = '';
            chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
            
            // Add to chatHistory
            chatHistory.push({ role: 'user', content: userMsg });
            
            // Show loading indicator in chatbot
            const loadingElement = document.getElementById('chatbot-loading');
            if (loadingElement) {
                loadingElement.style.display = 'block';
                chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
            }
            
            // Show loading spinner for recommendations section
            if (recLoading) recLoading.style.display = 'flex';
            
            try {
                // API call
                var response = await fetch('/cinema_chatbot_api/', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ history: chatHistory })
                });
                
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                
                var data = await response.json();
                console.log('Backend response:', data);
                
                // Hide loading indicators
                if (loadingElement) loadingElement.style.display = 'none';
                if (recLoading) recLoading.style.display = 'none';
                
                // Display bot response
                console.log('INLINE TEMPLATE SCRIPT - BOT MESSAGE:', data.message);
                var botDiv = document.createElement('div');
                botDiv.style.alignSelf = 'flex-start';
                var message = data.message;
                var trimmed = message && message.trim();
                if (trimmed && ((trimmed.startsWith('{') && trimmed.endsWith('}')) || /\{[\s\S]*?\}/.test(trimmed))) {
                  // Don't display anything
                } else {
                  botDiv.textContent = message;
                  botDiv.style.background = '#b61b23';
                  botDiv.style.color = '#fff';
                  botDiv.style.borderRadius = '12px';
                  botDiv.style.padding = '0.7rem 1rem';
                  botDiv.style.margin = '0.2rem 0';
                  botDiv.style.maxWidth = '85%';
                  chatbotMessages.appendChild(botDiv);
                }
                chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
                
                // Add to chatHistory
                chatHistory.push({ role: 'model', content: data.message });
                
                // Update movie display if recommendations are present
                if (data.recommendations && data.recommendations.length) {
                    updateNowShowing(data.recommendations);
                }
                
            } catch (error) {
                console.error('Chatbot API Error:', error);
                
                // Hide loading indicators
                if (loadingElement) loadingElement.style.display = 'none';
                if (recLoading) recLoading.style.display = 'none';
                
                // Display error message
                var errorDiv = document.createElement('div');
                errorDiv.style.alignSelf = 'flex-start';
                errorDiv.style.background = '#dc3545';
                errorDiv.style.color = '#fff';
                errorDiv.style.borderRadius = '12px';
                errorDiv.style.padding = '0.7rem 1rem';
                errorDiv.style.margin = '0.2rem 0';
                errorDiv.style.maxWidth = '85%';
                errorDiv.textContent = 'Sorry, I encountered an error. Please try again.';
                chatbotMessages.appendChild(errorDiv);
                chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
            }
        });
    }
}