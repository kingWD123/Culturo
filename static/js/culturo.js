/**
 * Culturo - JavaScript principal
 * Gestion des animations, interactions et fonctionnalités avancées
 */

class CulturoApp {
    constructor() {
        this.init();
    }

    init() {
        this.setupAnimations();
        this.setupInteractions();
        this.setupFormValidation();
        this.setupCulturalMatch();
        this.setupParallaxEffects();
    }

    // Animations et transitions
    setupAnimations() {
        // Intersection Observer pour les animations au scroll
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('fade-in');

                    // Animation spéciale pour les cartes
                    if (entry.target.classList.contains('card-hover')) {
                        this.animateCard(entry.target);
                    }
                }
            });
        }, observerOptions);

        // Observer tous les éléments avec animation
        document.querySelectorAll('.animate-on-scroll, .card-hover').forEach(el => {
            observer.observe(el);
        });

        // Animation des compteurs
        this.animateCounters();
    }

    // Animation des cartes
    animateCard(card) {
        const delay = Math.random() * 200;
        setTimeout(() => {
            card.style.transform = 'translateY(0) scale(1)';
            card.style.opacity = '1';
        }, delay);
    }

    // Animation des compteurs
    animateCounters() {
        const counters = document.querySelectorAll('[data-counter]');
        counters.forEach(counter => {
            const target = parseInt(counter.dataset.counter);
            const duration = 2000;
            const step = target / (duration / 16);
            let current = 0;

            const timer = setInterval(() => {
                current += step;
                if (current >= target) {
                    current = target;
                    clearInterval(timer);
                }
                counter.textContent = Math.round(current);
            }, 16);
        });
    }

    // Interactions utilisateur
    setupInteractions() {
        // Hover effects pour les cartes
        document.querySelectorAll('.card-hover').forEach(card => {
            card.addEventListener('mouseenter', (e) => {
                this.addHoverEffect(card);
            });

            card.addEventListener('mouseleave', (e) => {
                this.removeHoverEffect(card);
            });
        });

        // Smooth scrolling pour les ancres
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', (e) => {
                e.preventDefault();
                const target = document.querySelector(anchor.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });

        // Tooltips personnalisés
        this.setupTooltips();
    }

    // Effets de hover
    addHoverEffect(card) {
        card.style.transform = 'translateY(-8px) scale(1.02)';
        card.style.boxShadow = '0 20px 40px rgba(0, 0, 0, 0.15)';

        // Animation des icônes
        const icon = card.querySelector('i');
        if (icon) {
            icon.style.transform = 'rotate(12deg) scale(1.1)';
        }
    }

    removeHoverEffect(card) {
        card.style.transform = 'translateY(0) scale(1)';
        card.style.boxShadow = '0 4px 6px rgba(0, 0, 0, 0.1)';

        const icon = card.querySelector('i');
        if (icon) {
            icon.style.transform = 'rotate(0deg) scale(1)';
        }
    }

    // Tooltips
    setupTooltips() {
        const tooltipElements = document.querySelectorAll('[data-tooltip]');

        tooltipElements.forEach(element => {
            element.addEventListener('mouseenter', (e) => {
                this.showTooltip(e.target);
            });

            element.addEventListener('mouseleave', (e) => {
                this.hideTooltip();
            });
        });
    }

    showTooltip(element) {
        const tooltip = document.createElement('div');
        tooltip.className = 'culturo-tooltip';
        tooltip.textContent = element.dataset.tooltip;

        document.body.appendChild(tooltip);

        const rect = element.getBoundingClientRect();
        tooltip.style.left = rect.left + (rect.width / 2) - (tooltip.offsetWidth / 2) + 'px';
        tooltip.style.top = rect.top - tooltip.offsetHeight - 10 + 'px';

        setTimeout(() => tooltip.classList.add('show'), 10);
    }

    hideTooltip() {
        const tooltip = document.querySelector('.culturo-tooltip');
        if (tooltip) {
            tooltip.remove();
        }
    }

    // Validation des formulaires
    setupFormValidation() {
        const forms = document.querySelectorAll('form');

        forms.forEach(form => {
            form.addEventListener('submit', (e) => {
                if (!this.validateForm(form)) {
                    e.preventDefault();
                    this.showFormErrors(form);
                }
            });
        });
    }

    validateForm(form) {
        let isValid = true;
        const requiredFields = form.querySelectorAll('[required]');

        requiredFields.forEach(field => {
            if (!field.value.trim()) {
                isValid = false;
                field.classList.add('error');
            } else {
                field.classList.remove('error');
            }
        });

        // Validation spéciale pour les checkboxes
        const checkboxGroups = form.querySelectorAll('.checkbox-group');
        checkboxGroups.forEach(group => {
            const checkboxes = group.querySelectorAll('input[type="checkbox"]:checked');
            if (checkboxes.length === 0) {
                isValid = false;
                group.classList.add('error');
            } else {
                group.classList.remove('error');
            }
        });

        return isValid;
    }

    showFormErrors(form) {
        const errorMessage = document.createElement('div');
        errorMessage.className = 'form-error-message';
        errorMessage.innerHTML = '<i class="fas fa-exclamation-triangle"></i> Veuillez remplir tous les champs requis.';

        const existingError = form.querySelector('.form-error-message');
        if (existingError) {
            existingError.remove();
        }

        form.insertBefore(errorMessage, form.firstChild);

        setTimeout(() => {
            errorMessage.remove();
        }, 5000);
    }

    // Calcul de compatibilité culturelle
    setupCulturalMatch() {
        const matchElements = document.querySelectorAll('[data-cultural-match]');

        matchElements.forEach(element => {
            const score = this.calculateCulturalMatch(element.dataset.culturalMatch);
            this.animateMatchScore(element, score);
        });
    }

    calculateCulturalMatch(preferences) {
        // Algorithme simple de calcul de compatibilité
        const prefs = JSON.parse(preferences);
        let score = 0;

        if (prefs.music && prefs.music.length > 0) score += 25;
        if (prefs.film && prefs.film.length > 0) score += 25;
        if (prefs.cuisine && prefs.cuisine.length > 0) score += 25;
        if (prefs.activities && prefs.activities.length > 0) score += 25;

        return Math.min(score, 100);
    }

    animateMatchScore(element, targetScore) {
        let currentScore = 0;
        const increment = targetScore / 20;

        const timer = setInterval(() => {
            currentScore += increment;
            if (currentScore >= targetScore) {
                currentScore = targetScore;
                clearInterval(timer);
            }

            element.textContent = Math.round(currentScore) + '%';
            element.style.color = this.getScoreColor(currentScore);
        }, 50);
    }

    getScoreColor(score) {
        if (score >= 80) return '#10b981'; // Vert
        if (score >= 60) return '#f59e0b'; // Orange
        return '#ef4444'; // Rouge
    }

    // Effets parallax
    setupParallaxEffects() {
        const parallaxElements = document.querySelectorAll('[data-parallax]');

        window.addEventListener('scroll', () => {
            const scrolled = window.pageYOffset;

            parallaxElements.forEach(element => {
                const speed = element.dataset.parallax || 0.5;
                const yPos = -(scrolled * speed);
                element.style.transform = `translateY(${yPos}px)`;
            });
        });
    }

    // Gestion des messages
    showMessage(message, type = 'info') {
        const messageElement = document.createElement('div');
        messageElement.className = `culturo-message culturo-message-${type}`;
        messageElement.innerHTML = `
            <i class="fas fa-${this.getMessageIcon(type)}"></i>
            <span>${message}</span>
            <button onclick="this.parentElement.remove()">
                <i class="fas fa-times"></i>
            </button>
        `;

        document.body.appendChild(messageElement);

        setTimeout(() => {
            messageElement.classList.add('show');
        }, 10);

        setTimeout(() => {
            messageElement.classList.remove('show');
            setTimeout(() => messageElement.remove(), 300);
        }, 5000);
    }

    getMessageIcon(type) {
        const icons = {
            success: 'check-circle',
            error: 'exclamation-circle',
            warning: 'exclamation-triangle',
            info: 'info-circle'
        };
        return icons[type] || 'info-circle';
    }

    // API calls
    async fetchCulturalMatch(preferences) {
        try {
            const response = await fetch('/api/cultural-match/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCSRFToken()
                },
                body: JSON.stringify({ preferences })
            });

            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Erreur lors du calcul de compatibilité:', error);
            return null;
        }
    }

    getCSRFToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]')?.value || '';
    }

    // Utilitaires
    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    throttle(func, limit) {
        let inThrottle;
        return function () {
            const args = arguments;
            const context = this;
            if (!inThrottle) {
                func.apply(context, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        }
    }
}

// === Chatbot Gemini pour la page cinéma ===
(function () {
    const input = document.getElementById('chatbot-input');
    const sendBtn = document.getElementById('chatbot-send');
    const messagesDiv = document.getElementById('chatbot-messages');
    const form = document.getElementById('chatbot-form');
    if (!input || !sendBtn || !messagesDiv || !form) return;

    let history = [];
    let isBotTyping = false;

    function showTypingIndicator() {
        const typingDiv = document.createElement('div');
        typingDiv.className = 'bot-message typing-indicator-container';
        typingDiv.id = 'typing-indicator';
        typingDiv.innerHTML = '<span class="typing-indicator"><span></span><span></span><span></span></span>';
        messagesDiv.appendChild(typingDiv);
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    }
    function removeTypingIndicator() {
        const typingDiv = document.getElementById('typing-indicator');
        if (typingDiv) typingDiv.remove();
    }
    function appendUserMessage(message) {
        const userDiv = document.createElement('div');
        userDiv.className = 'user-message';
        userDiv.textContent = message;
        messagesDiv.appendChild(userDiv);
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    }
    function appendBotMessageAnimated(message) {
        const botDiv = document.createElement('div');
        botDiv.className = 'bot-message';
        messagesDiv.appendChild(botDiv);
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
        let i = 0;
        function typeChar() {
            if (i <= message.length) {
                botDiv.textContent = message.slice(0, i);
                messagesDiv.scrollTop = messagesDiv.scrollHeight;
                i++;
                setTimeout(typeChar, 12 + Math.random() * 18); // effet naturel
            }
        }
        typeChar();
    }

    async function sendMessage() {
        const message = input.value.trim();
        if (!message || isBotTyping) return;
        appendUserMessage(message);
        input.value = "";
        history.push({ role: "user", content: message });
        showTypingIndicator();
        isBotTyping = true;
        try {
            const response = await fetch('/cinema_chatbot_api/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ history: history })
            });
            const data = await response.json();
            removeTypingIndicator();
            appendBotMessageAnimated(data.message);
            history.push({ role: "assistant", content: data.message });
            
            // Affichage des données utilisateur si disponibles
            if (data.done && data.user_data) {
                const userDataDiv = document.createElement('div');
                userDataDiv.className = 'bot-message user-data-display';
                userDataDiv.innerHTML = `
                    <h4>📊 Vos Préférences Collectées :</h4>
                    <div style="background: #f8f9fa; border-radius: 10px; padding: 0.7rem 1rem; margin: 8px 0;">
                        <strong>Genre :</strong> ${data.user_data.genre || 'Non spécifié'}<br>
                        <strong>Langue :</strong> ${data.user_data.langue || 'Non spécifié'}<br>
                        <strong>Plateforme :</strong> ${data.user_data.plateforme || 'Non spécifié'}<br>
                        <strong>Âge :</strong> ${data.user_data.age || 'Non spécifié'}<br>
                        <strong>Pays :</strong> ${data.user_data.pays || 'Non spécifié'}
                    </div>
                `;
                messagesDiv.appendChild(userDataDiv);
                messagesDiv.scrollTop = messagesDiv.scrollHeight;
            }
            
            // Affichage de l'URL Qloo générée
            if (data.qloo_url) {
                const qlooUrlDiv = document.createElement('div');
                qlooUrlDiv.className = 'bot-message qloo-url-display';
                qlooUrlDiv.innerHTML = `
                    <h4>🔗 URL Qloo API Générée :</h4>
                    <div style="background: #e3f2fd; border-radius: 10px; padding: 0.7rem 1rem; margin: 8px 0; word-break: break-all; font-family: monospace; font-size: 0.9rem;">
                        ${data.qloo_url}
                    </div>
                `;
                messagesDiv.appendChild(qlooUrlDiv);
                messagesDiv.scrollTop = messagesDiv.scrollHeight;
            }
            
            // Affichage de la réponse de l'API Qloo et mise à jour de la section Now Showing
            if (data.qloo_response) {
                // Message simple dans le chatbot
                const qlooResponseDiv = document.createElement('div');
                qlooResponseDiv.className = 'bot-message qloo-response-display';
                
                if (data.qloo_response.success) {
                    qlooResponseDiv.innerHTML = `
                        <h4>🎬 Recommandations générées !</h4>
                        <div style="background: #e8f5e8; border-radius: 10px; padding: 0.7rem 1rem; margin: 8px 0;">
                            <p>Vos recommandations personnalisées ont été ajoutées à la section "Now Showing" ci-dessous !</p>
                            <div style="margin-top: 12px; font-size: 0.9rem; color: #666; text-align: center;">
                                ${data.qloo_response.data.source === 'demo_mode' ? 
                                    '🎭 Mode démo - Recommandations basées sur vos préférences' : 
                                    '✅ Données réelles de l\'API Qloo'
                                }
                            </div>
                            <div style="margin-top: 16px; text-align: center;">
                                <button onclick="showMoreRecommendations('${data.qloo_response.data.source === 'demo_mode' ? 'demo' : 'api'}')" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 8px 16px; border-radius: 20px; text-decoration: none; font-weight: 600; display: inline-block; transition: all 0.3s ease; border: none; cursor: pointer; font-size: 0.9rem;">
                                    🎬 Voir Plus de Films
                                </button>
                            </div>
                        </div>
                    `;
                    
                    // Mise à jour dynamique de la section Now Showing
                    updateNowShowingSection(data.qloo_response);
                } else {
                    // Affichage des erreurs
                    qlooResponseDiv.innerHTML = `
                        <h4>❌ Erreur API Qloo :</h4>
                        <div style="background: #ffebee; border-radius: 10px; padding: 0.7rem 1rem; margin: 8px 0;">
                            <strong>Erreur :</strong> ${data.qloo_response.error}<br>
                            <strong>Statut :</strong> ${data.qloo_response.status_code || 'N/A'}<br>
                            <strong>Détails :</strong> ${data.qloo_response.response_text || 'Aucun détail'}
                        </div>
                    `;
                }
                messagesDiv.appendChild(qlooResponseDiv);
                messagesDiv.scrollTop = messagesDiv.scrollHeight;
            }
            
        } catch (e) {
            removeTypingIndicator();
            appendBotMessageAnimated("Erreur lors de la connexion au chatbot.");
            console.error("Erreur chatbot:", e);
        }
        isBotTyping = false;
    }

    sendBtn.onclick = function (e) {
        e.preventDefault();
        sendMessage();
    };
    form.addEventListener('submit', function (e) {
        e.preventDefault();
        sendMessage();
    });
    input.addEventListener('keydown', function (e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            sendMessage();
        }
    });
})();

// Fonction pour mettre à jour dynamiquement la section Now Showing
function updateNowShowingSection(qlooResponse) {
    const nowShowingGrid = document.querySelector('.cinema-movies-grid');
    if (!nowShowingGrid) return;

    console.log("=== DEBUG: Données reçues de l'API ===");
    console.log("qlooResponse:", qlooResponse);
    console.log("qlooResponse.data:", qlooResponse.data);
    console.log("Type de qlooResponse.data:", typeof qlooResponse.data);
    if (qlooResponse.data) {
        console.log("Clés disponibles:", Object.keys(qlooResponse.data));
        if (qlooResponse.data.recommendations) {
            console.log("Première recommandation:", qlooResponse.data.recommendations[0]);
        }
        if (qlooResponse.data.entities) {
            console.log("Première entité:", qlooResponse.data.entities[0]);
        }
    }
    console.log("=====================================");

    // Données de démonstration pour plus de recommandations
    const demoRecommendations = [
        {
            title: "Inception",
            year: 2010,
            rating: 8.8,
            language: "Anglais",
            genre: "Science-Fiction",
            director: "Christopher Nolan",
            description: "Un thriller de science-fiction révolutionnaire sur les rêves et la réalité.",
            image: "https://images.unsplash.com/photo-1517602302552-471fe67acf66?auto=format&fit=crop&w=400&q=80"
        },
        {
            title: "Parasite",
            year: 2019,
            rating: 8.6,
            language: "Coréen",
            genre: "Thriller",
            director: "Bong Joon-ho",
            description: "Un film acclamé qui explore les inégalités sociales avec humour noir.",
            image: "https://images.unsplash.com/photo-1504384308090-c894fdcc538d?auto=format&fit=crop&w=400&q=80"
        },
        {
            title: "La La Land",
            year: 2016,
            rating: 8.0,
            language: "Anglais",
            genre: "Comédie musicale",
            director: "Damien Chazelle",
            description: "Une romance musicale moderne qui célèbre les rêves d'Hollywood.",
            image: "https://images.unsplash.com/photo-1465101046530-c894fdcc538d?auto=format&fit=crop&w=400&q=80"
        },
        {
            title: "Spirited Away",
            year: 2001,
            rating: 8.6,
            language: "Japonais",
            genre: "Animation",
            director: "Hayao Miyazaki",
            description: "Un chef-d'œuvre d'animation japonaise sur la magie et l'aventure.",
            image: "https://images.unsplash.com/photo-1468071174046-657d9d351a40?auto=format&fit=crop&w=400&q=80"
        }
    ];

    const apiRecommendations = [
        {
            name: "The Matrix",
            id: "movie_001",
            type: "movie",
            score: 0.95,
            metadata: { year: 1999, rating: 8.7 },
            image_url: "https://images.unsplash.com/photo-1517602302552-471fe67acf66?auto=format&fit=crop&w=400&q=80"
        },
        {
            name: "Pulp Fiction",
            id: "movie_002",
            type: "movie",
            score: 0.92,
            metadata: { year: 1994, rating: 8.9 },
            image_url: "https://images.unsplash.com/photo-1504384308090-c894fdcc538d?auto=format&fit=crop&w=400&q=80"
        },
        {
            name: "Fight Club",
            id: "movie_003",
            type: "movie",
            score: 0.89,
            metadata: { year: 1999, rating: 8.8 },
            image_url: "https://images.unsplash.com/photo-1465101046530-c894fdcc538d?auto=format&fit=crop&w=400&q=80"
        },
        {
            name: "The Godfather",
            id: "movie_004",
            type: "movie",
            score: 0.96,
            metadata: { year: 1972, rating: 9.2 },
            image_url: "https://images.unsplash.com/photo-1468071174046-657d9d351a40?auto=format&fit=crop&w=400&q=80"
        }
    ];

    let recommendations = [];
    
    if (qlooResponse.data.recommendations) {
        // Mode démo - données structurées avec title, year, rating
        recommendations = qlooResponse.data.recommendations;
        console.log("Mode démo détecté:", recommendations);
    } else if (qlooResponse.data.entities) {
        // Données API Qloo - format entities
        recommendations = qlooResponse.data.entities;
        console.log("Mode API Qloo détecté:", recommendations);
    } else if (qlooResponse.data && Array.isArray(qlooResponse.data)) {
        // Données API Qloo - format array direct
        recommendations = qlooResponse.data;
        console.log("Mode API Qloo (array) détecté:", recommendations);
    } else {
        // Fallback vers les données de démo
        console.log("Fallback vers données de démo");
        recommendations = demoRecommendations;
    }

    // Vider la grille existante
    nowShowingGrid.innerHTML = '';

    // Ajouter les nouvelles recommandations
    recommendations.forEach((movie, index) => {
        const movieCard = document.createElement('div');
        movieCard.className = 'cinema-movie-card';
        movieCard.style.animation = `fadeInUp 0.6s ease ${index * 0.1}s both`;
        
        let title, year, rating, imageUrl;
        
        // Détection du type de données
        if (movie.title && movie.year && movie.rating) {
            // Mode démo - données structurées
            title = movie.title;
            year = movie.year;
            rating = movie.rating;
            imageUrl = movie.image || movie.image_url || `https://images.unsplash.com/photo-${1517602302552 + index}?auto=format&fit=crop&w=400&q=80`;
        } else if (movie.name || movie.title) {
            // Mode API Qloo - format entities
            title = movie.name || movie.title || 'Film';
            
            // Extraction de l'année depuis metadata ou autres champs
            if (movie.metadata && movie.metadata.year) {
                year = movie.metadata.year;
            } else if (movie.year) {
                year = movie.year;
            } else if (movie.release_date) {
                year = new Date(movie.release_date).getFullYear();
            } else {
                year = 'N/A';
            }
            
            // Extraction de la note depuis metadata ou autres champs
            if (movie.metadata && movie.metadata.rating) {
                rating = movie.metadata.rating;
            } else if (movie.rating) {
                rating = movie.rating;
            } else if (movie.score) {
                rating = (movie.score * 10).toFixed(1);
            } else {
                rating = 'N/A';
            }
            
            // Extraction de l'image depuis différents champs possibles
            imageUrl = movie.image_url || movie.poster_url || movie.thumbnail || movie.image || movie.poster || `https://images.unsplash.com/photo-${1517602302552 + index}?auto=format&fit=crop&w=400&q=80`;
        } else {
            // Fallback pour données inconnues
            title = 'Film Inconnu';
            year = 'N/A';
            rating = 'N/A';
            imageUrl = `https://images.unsplash.com/photo-${1517602302552 + index}?auto=format&fit=crop&w=400&q=80`;
        }

        movieCard.innerHTML = `
            <img src="${imageUrl}" alt="${title}" class="cinema-movie-img">
            <div class="cinema-movie-info">
                <h4>"${title}"</h4>
                <span class="cinema-movie-date">${year} • ⭐ ${rating}/10</span>
                <a href="#" class="btn btn-secondary">Discover</a>
            </div>
        `;
        
        nowShowingGrid.appendChild(movieCard);
    });

    // Ajouter les styles d'animation si pas déjà présents
    if (!document.getElementById('cinema-animations')) {
        const style = document.createElement('style');
        style.id = 'cinema-animations';
        style.textContent = `
            @keyframes fadeInUp {
                from {
                    opacity: 0;
                    transform: translateY(30px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
        `;
        document.head.appendChild(style);
    }

    // Faire défiler vers la section Now Showing
    const nowShowingSection = document.getElementById('now-showing');
    if (nowShowingSection) {
        nowShowingSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
}

// Fonction pour afficher plus de recommandations dans la section Now Showing
function showMoreRecommendations(type) {
    // Créer un objet de réponse simulé pour utiliser updateNowShowingSection
    const mockResponse = {
        data: {
            recommendations: type === 'demo' ? [
                {
                    title: "The Grand Budapest Hotel",
                    year: 2014,
                    rating: 8.1,
                    language: "Anglais",
                    genre: "Comédie",
                    director: "Wes Anderson",
                    description: "Une comédie excentrique avec une esthétique visuelle unique.",
                    image: "https://images.unsplash.com/photo-1517602302552-471fe67acf66?auto=format&fit=crop&w=400&q=80"
                },
                {
                    title: "Amélie",
                    year: 2001,
                    rating: 8.3,
                    language: "Français",
                    genre: "Comédie romantique",
                    director: "Jean-Pierre Jeunet",
                    description: "Un film français charmant sur l'amour et la magie du quotidien.",
                    image: "https://images.unsplash.com/photo-1504384308090-c894fdcc538d?auto=format&fit=crop&w=400&q=80"
                },
                {
                    title: "Blade Runner 2049",
                    year: 2017,
                    rating: 8.0,
                    language: "Anglais",
                    genre: "Science-Fiction",
                    director: "Denis Villeneuve",
                    description: "Une suite visuellement époustouflante du classique de science-fiction.",
                    image: "https://images.unsplash.com/photo-1465101046530-c894fdcc538d?auto=format&fit=crop&w=400&q=80"
                },
                {
                    title: "Mad Max: Fury Road",
                    year: 2015,
                    rating: 8.1,
                    language: "Anglais",
                    genre: "Action",
                    director: "George Miller",
                    description: "Un film d'action post-apocalyptique spectaculaire.",
                    image: "https://images.unsplash.com/photo-1468071174046-657d9d351a40?auto=format&fit=crop&w=400&q=80"
                }
            ] : [
                {
                    name: "Interstellar",
                    id: "movie_005",
                    type: "movie",
                    score: 0.88,
                    metadata: { year: 2014, rating: 8.6 },
                    image_url: "https://images.unsplash.com/photo-1517602302552-471fe67acf66?auto=format&fit=crop&w=400&q=80"
                },
                {
                    name: "The Dark Knight",
                    id: "movie_006",
                    type: "movie",
                    score: 0.94,
                    metadata: { year: 2008, rating: 9.0 },
                    image_url: "https://images.unsplash.com/photo-1504384308090-c894fdcc538d?auto=format&fit=crop&w=400&q=80"
                },
                {
                    name: "Inception",
                    id: "movie_007",
                    type: "movie",
                    score: 0.91,
                    metadata: { year: 2010, rating: 8.8 },
                    image_url: "https://images.unsplash.com/photo-1465101046530-c894fdcc538d?auto=format&fit=crop&w=400&q=80"
                },
                {
                    name: "The Shawshank Redemption",
                    id: "movie_008",
                    type: "movie",
                    score: 0.97,
                    metadata: { year: 1994, rating: 9.3 },
                    image_url: "https://images.unsplash.com/photo-1468071174046-657d9d351a40?auto=format&fit=crop&w=400&q=80"
                }
            ]
        }
    };

    // Mettre à jour la section Now Showing avec les nouvelles recommandations
    updateNowShowingSection(mockResponse);

    // Afficher un message dans le chatbot pour confirmer
    const messagesDiv = document.getElementById('chatbot-messages');
    if (messagesDiv) {
        const confirmDiv = document.createElement('div');
        confirmDiv.className = 'bot-message';
        confirmDiv.innerHTML = `
            <h4>🎬 Plus de Recommandations Ajoutées !</h4>
            <div style="background: #e8f5e8; border-radius: 10px; padding: 0.7rem 1rem; margin: 8px 0;">
                <p>De nouvelles recommandations ont été ajoutées à la section "Now Showing" !</p>
                <div style="margin-top: 12px; font-size: 0.9rem; color: #666; text-align: center;">
                    ${type === 'demo' ? '🎭 Mode démo - Recommandations supplémentaires' : '✅ Données API Qloo supplémentaires'}
                </div>
            </div>
        `;
        messagesDiv.appendChild(confirmDiv);
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    }
}

// Initialisation de l'application
document.addEventListener('DOMContentLoaded', () => {
    window.culturoApp = new CulturoApp();
});

// Styles CSS pour les composants JavaScript
const styles = `
    .culturo-tooltip {
        position: absolute;
        background: rgba(0, 0, 0, 0.8);
        color: white;
        padding: 8px 12px;
        border-radius: 6px;
        font-size: 14px;
        z-index: 1000;
        opacity: 0;
        transform: translateY(10px);
        transition: all 0.3s ease;
        pointer-events: none;
    }

    .culturo-tooltip.show {
        opacity: 1;
        transform: translateY(0);
    }

    .culturo-tooltip::after {
        content: '';
        position: absolute;
        top: 100%;
        left: 50%;
        transform: translateX(-50%);
        border: 5px solid transparent;
        border-top-color: rgba(0, 0, 0, 0.8);
    }

    .form-error-message {
        background: #fef2f2;
        border: 1px solid #fecaca;
        color: #dc2626;
        padding: 12px;
        border-radius: 8px;
        margin-bottom: 16px;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .culturo-message {
        position: fixed;
        top: 20px;
        right: 20px;
        background: white;
        border-radius: 8px;
        padding: 16px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        z-index: 1000;
        display: flex;
        align-items: center;
        gap: 12px;
        transform: translateX(100%);
        transition: transform 0.3s ease;
    }

    .culturo-message.show {
        transform: translateX(0);
    }

    .culturo-message-success {
        border-left: 4px solid #10b981;
    }

    .culturo-message-error {
        border-left: 4px solid #ef4444;
    }

    .culturo-message-warning {
        border-left: 4px solid #f59e0b;
    }

    .culturo-message-info {
        border-left: 4px solid #3b82f6;
    }

    .culturo-message button {
        background: none;
        border: none;
        cursor: pointer;
        color: #6b7280;
        padding: 4px;
        border-radius: 4px;
        transition: background-color 0.2s;
    }

    .culturo-message button:hover {
        background-color: #f3f4f6;
    }

    .error {
        border-color: #ef4444 !important;
        box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.1) !important;
    }

    .recommendation-card {
        background: white;
        border-radius: 12px;
        padding: 16px;
        margin: 12px 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        border-left: 4px solid #667eea;
        transition: all 0.3s ease;
    }

    .recommendation-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.15);
    }

    .recommendation-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 16px;
        margin-top: 16px;
    }

    .recommendation-item {
        background: #f8f9fa;
        border-radius: 8px;
        padding: 12px;
        border: 1px solid #e9ecef;
        transition: all 0.3s ease;
    }

    .recommendation-item:hover {
        background: #e9ecef;
        transform: translateY(-1px);
    }

    .checkbox-group.error {
        border: 2px solid #ef4444;
        border-radius: 8px;
        padding: 8px;
    }
`;

// Injection des styles
const styleSheet = document.createElement('style');
styleSheet.textContent = styles;
document.head.appendChild(styleSheet); 