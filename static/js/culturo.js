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
            if (data.done && data.user_data) {
                const pre = document.createElement('pre');
                pre.textContent = JSON.stringify(data.user_data, null, 2);
                pre.style.background = '#f8f9fa';
                pre.style.borderRadius = '10px';
                pre.style.padding = '0.7rem 1rem';
                pre.style.margin = '8px 0 0 0';
                pre.style.fontSize = '0.98rem';
                messagesDiv.appendChild(pre);
                messagesDiv.scrollTop = messagesDiv.scrollHeight;
            }
            // Ajout dynamique des films Now Showing
            if (data.qloo_url) {
                fetch('/api/get_movies_from_qloo/', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ qloo_url: data.qloo_url })
                })
                .then(res => res.json())
                .then(resData => {
                    const allMovies = resData.movies || [];
                    updateNowShowing(allMovies);
                })
                .catch(() => {
                    const grid = document.querySelector('.cinema-movies-grid');
                    if (grid) grid.innerHTML = '<div style="padding:1rem;">Erreur lors du chargement des films.</div>';
                });
            }
        } catch (e) {
            removeTypingIndicator();
            appendBotMessageAnimated("Erreur lors de la connexion au chatbot.");
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

// Initialisation de l'application
document.addEventListener('DOMContentLoaded', () => {
    window.culturoApp = new CulturoApp();
});

// Styles CSS pour les composants JavaScript
const styles = `
    .culturo-tooltip {
        position: absolute;
        background: rgba(20, 20, 20, 0.98); /* Netflix dark */
        color: #fff;
        padding: 10px 16px;
        border-radius: 8px;
        font-size: 15px;
        z-index: 1000;
        opacity: 0;
        transform: translateY(10px);
        transition: all 0.3s cubic-bezier(.4,0,.2,1);
        pointer-events: none;
        box-shadow: 0 4px 24px rgba(0,0,0,0.5);
        font-family: 'Roboto', Arial, sans-serif;
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
        border: 6px solid transparent;
        border-top-color: rgba(20, 20, 20, 0.98);
    }

    .form-error-message {
        background: #2d2d2d;
        border: 1px solid #e50914;
        color: #fff;
        padding: 14px;
        border-radius: 8px;
        margin-bottom: 18px;
        display: flex;
        align-items: center;
        gap: 10px;
        font-family: 'Roboto', Arial, sans-serif;
    }

    .culturo-message {
        position: fixed;
        top: 24px;
        right: 24px;
        background: #181818;
        border-radius: 10px;
        padding: 18px;
        box-shadow: 0 6px 24px rgba(0,0,0,0.5);
        z-index: 1000;
        display: flex;
        align-items: center;
        gap: 14px;
        transform: translateX(100%);
        transition: transform 0.3s cubic-bezier(.4,0,.2,1);
        color: #fff;
        font-family: 'Roboto', Arial, sans-serif;
    }

    .culturo-message.show {
        transform: translateX(0);
    }

    .culturo-message-success {
        border-left: 5px solid #46d369;
    }

    .culturo-message-error {
        border-left: 5px solid #e50914;
    }

    .culturo-message-warning {
        border-left: 5px solid #f59e0b;
    }

    .culturo-message-info {
        border-left: 5px solid #3b82f6;
    }

    .culturo-message button {
        background: none;
        border: none;
        cursor: pointer;
        color: #fff;
        padding: 4px;
        border-radius: 4px;
        transition: background-color 0.2s;
    }

    .culturo-message button:hover {
        background-color: #e50914;
        color: #fff;
    }

    .error {
        border-color: #e50914 !important;
        box-shadow: 0 0 0 3px rgba(229, 9, 20, 0.15) !important;
    }

    .checkbox-group.error {
        border: 2px solid #e50914;
        border-radius: 8px;
        padding: 8px;
        background: #181818;
    }

    /* Netflix-style movie cards */
    .cinema-movie-card {
        background: #181818;
        border-radius: 12px;
        box-shadow: 0 2px 16px rgba(0,0,0,0.7);
        overflow: hidden;
        transition: transform 0.2s, box-shadow 0.2s;
        color: #fff;
        font-family: 'Roboto', Arial, sans-serif;
    }
    .cinema-movie-card:hover {
        transform: scale(1.04) translateY(-6px);
        box-shadow: 0 8px 32px rgba(229,9,20,0.25);
        border: 2px solid #e50914;
    }
    .cinema-movie-img {
        width: 100%;
        height: 260px;
        object-fit: cover;
        border-top-left-radius: 12px;
        border-top-right-radius: 12px;
        background: #222;
    }
    .cinema-movie-info {
        padding: 18px 14px 14px 14px;
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        gap: 8px;
    }
    .cinema-movie-info h4 {
        font-size: 1.1rem;
        font-weight: 500;
        margin: 0;
        color: #fff;
    }
    .cinema-movie-date {
        font-size: 0.95rem;
        color: #b3b3b3;
    }
    .discover-btn {
        background: #e50914;
        color: #fff;
        border: none;
        border-radius: 6px;
        padding: 8px 18px;
        font-size: 1rem;
        font-weight: 500;
        margin-top: 8px;
        cursor: pointer;
        transition: background 0.2s, color 0.2s;
        box-shadow: 0 2px 8px rgba(229,9,20,0.08);
    }
    .discover-btn:hover {
        background: #b0060f;
        color: #fff;
    }
    /* Pagination */
    #now-showing-pagination button {
        background: #232323;
        color: #fff;
        border: none;
        border-radius: 6px;
        padding: 8px 18px;
        font-size: 1rem;
        font-weight: 500;
        cursor: pointer;
        transition: background 0.2s, color 0.2s;
        margin: 0 4px;
    }
    #now-showing-pagination button:hover {
        background: #e50914;
        color: #fff;
    }
`;

// Injection des styles
const styleSheet = document.createElement('style');
styleSheet.textContent = styles;
document.head.appendChild(styleSheet);

// Section Now Showing : affichage par défaut de films populaires si aucune recommandation
/*
const defaultMovies = [
    {
        name: "The Godfather",
        release_year: 1972,
        image_url: "https://postercinema.eu/cdn/shop/files/the-godfather_4f919463.jpg?v=1707474775",
    },
    {
        name: "Inception",
        release_year: 2010,
        image_url: "https://play-lh.googleusercontent.com/-qtECEmfe9yjg9w57QlILDP8Bgk5mT-cOUduloX_48y_NGYaP4dgZnrY0tUP7WX5x-vXEKhOzWL-QgFXyp4=w240-h480-rw",
    },
    {
        name: "Amélie (Le Fabuleux Destin d'Amélie Poulain)",
        release_year: 2001,
        image_url: "https://fr.web.img2.acsta.net/img/14/28/14285c344d92ed68b26bffc6afbca358.jpg",
    },
    {
        name: "Parasite",
        release_year: 2019,
        image_url: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTTHqERudQeMKbEpp97lLK_unmW1aJZLdP_-A&s",
    },
    {
        name: "Interstellar",
        release_year: 2014,
        image_url: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQfw8Ic__jQPSqabC3yvz0-CMMZ1_eZKN41DQ&s",
    },
];
*/

// Fonction pour afficher une liste de films dans Now Showing
function renderNowShowing(movies) {
    const grid = document.querySelector('.cinema-movies-grid');
    if (!grid) return;
    grid.innerHTML = '';
    let allMovies = movies || [];
    let currentPage = 0;
    const pageSize = 10;
    function renderPage(page) {
        grid.innerHTML = '';
        const start = page * pageSize;
        const end = Math.min(start + pageSize, allMovies.length);
        for (let i = start; i < end; i++) {
            const movie = allMovies[i];
            if (movie.entity_id) {
                try {
                    localStorage.setItem('movie_' + movie.entity_id, JSON.stringify(movie));
                } catch (e) {}
            }
            const imgSrc = movie.image_url || (movie.image && movie.image.url) || movie.image || '';
            const card = document.createElement('div');
            card.className = 'cinema-movie-card';
            card.innerHTML = `
                <img src="${imgSrc}" alt="${movie.name || ''}" class="cinema-movie-img">
                <div class="cinema-movie-info" style="align-items: center;">
                    <h4 style="width: 100%; text-align: center; margin-bottom: 0.3em;">${movie.name || ''}</h4>
                    <span class="cinema-movie-date" style="width: 100%; text-align: center;">${movie.release_year || ''}</span>
                    <a href="#" class="btn btn-secondary discover-btn" data-entity-id="${movie.entity_id || ''}">Discover</a>
                </div>
            `;
            grid.appendChild(card);
        }
        // Ajout du handler Discover
        setTimeout(() => {
            document.querySelectorAll('.discover-btn').forEach(btn => {
                btn.onclick = function(e) {
                    e.preventDefault();
                    const entityId = btn.getAttribute('data-entity-id');
                    if (entityId) {
                        window.location.href = `/movie_detail/?id=${encodeURIComponent(entityId)}`;
                    }
                };
            });
        }, 10);
        // Pagination controls
        let controls = document.getElementById('now-showing-pagination');
        if (!controls) {
            controls = document.createElement('div');
            controls.id = 'now-showing-pagination';
            controls.style.display = 'flex';
            controls.style.justifyContent = 'center';
            controls.style.gap = '2.5rem';
            controls.style.margin = '1.5rem 0 0 0';
            grid.parentElement.appendChild(controls);
        }
        controls.innerHTML = '';
        if (page > 0) {
            const prevBtn = document.createElement('button');
            prevBtn.textContent = 'Précédent';
            prevBtn.className = 'btn btn-secondary';
            prevBtn.onclick = () => {
                currentPage--;
                renderPage(currentPage);
            };
            controls.appendChild(prevBtn);
        }
        if (end < allMovies.length) {
            const nextBtn = document.createElement('button');
            nextBtn.textContent = 'Suivant';
            nextBtn.className = 'btn btn-secondary';
            nextBtn.onclick = () => {
                currentPage++;
                renderPage(currentPage);
            };
            controls.appendChild(nextBtn);
        }
        if (allMovies.length === 0) {
            grid.innerHTML = '<div style="padding:1rem;">Aucun film trouvé.</div>';
            controls.innerHTML = '';
        }
    }
    // Désactivation de l'affichage par défaut
    // renderPage(currentPage);
}

// Affichage par défaut au chargement (désactivé, rendu côté serveur)
// window.addEventListener('DOMContentLoaded', function() {
//     renderNowShowing(defaultMovies);
// });

// Fonction pour afficher dynamiquement une liste de films dans Now Showing
function updateNowShowing(movies) {
    const grid = document.querySelector('.cinema-movies-grid');
    if (!grid) return;
    grid.innerHTML = '';
    // Pagination
    const pageSize = 5;
    let currentPage = 0;
    function renderPage(page) {
        grid.innerHTML = '';
        const start = page * pageSize;
        const end = Math.min(start + pageSize, movies.length);
        for (let i = start; i < end; i++) {
            const film = movies[i];
            let imgSrc = '';
            if (film.image) {
                if (typeof film.image === 'string') {
                    imgSrc = film.image;
                } else if (film.image.url) {
                    imgSrc = film.image.url;
                }
            } else if (film.image_url) {
                imgSrc = film.image_url;
            } else if (film.properties && film.properties.image && film.properties.image.url) {
                imgSrc = film.properties.image.url;
            }
            if (!imgSrc) {
                imgSrc = '/static/images/film-placeholder.png';
            }
            // Stockage local pour fallback page détail (entity_id, imdb_id, slug)
            if (film.entity_id) {
                try { localStorage.setItem('movie_' + film.entity_id, JSON.stringify(film)); } catch (e) {}
            }
            if (film.imdb_id) {
                try { localStorage.setItem('movie_' + film.imdb_id, JSON.stringify(film)); } catch (e) {}
            }
            if (film.name) {
                const slug = film.name.replace(/\s+/g, '-').toLowerCase();
                try { localStorage.setItem('movie_' + slug, JSON.stringify(film)); } catch (e) {}
            }
            // Choix de l'identifiant pour la page de détail
            let detailId = film.entity_id || film.imdb_id || (film.name ? film.name.replace(/\s+/g, '-').toLowerCase() : '');
            const card = document.createElement('div');
            card.className = 'cinema-movie-card';
            card.innerHTML = `
                <img src="${imgSrc}" alt="${film.name || ''}" class="cinema-movie-img">
                <div class="cinema-movie-info">
                    <h4>${film.name || ''}</h4>
                    ${film.release_year ? `<span class="cinema-movie-date">${film.release_year}</span>` : ''}
                    <a href="/movie_detail/?id=${encodeURIComponent(detailId)}" class="btn btn-secondary">Discover</a>
                </div>
            `;
            grid.appendChild(card);
        }
        // Pagination controls
        let controls = document.getElementById('now-showing-pagination');
        if (!controls) {
            controls = document.createElement('div');
            controls.id = 'now-showing-pagination';
            controls.style.display = 'flex';
            controls.style.justifyContent = 'center';
            controls.style.gap = '2.5rem';
            controls.style.margin = '1.5rem 0 0 0';
            grid.parentElement.appendChild(controls);
        }
        controls.innerHTML = '';
        if (page > 0) {
            const prevBtn = document.createElement('button');
            prevBtn.textContent = 'Précédent';
            prevBtn.className = 'btn btn-secondary';
            prevBtn.onclick = () => {
                currentPage--;
                renderPage(currentPage);
            };
            controls.appendChild(prevBtn);
        }
        if (end < movies.length) {
            const nextBtn = document.createElement('button');
            nextBtn.textContent = 'Suivant';
            nextBtn.className = 'btn btn-secondary';
            nextBtn.onclick = () => {
                currentPage++;
                renderPage(currentPage);
            };
            controls.appendChild(nextBtn);
        }
        if (movies.length === 0) {
            grid.innerHTML = '<div style="color:#fff;">No recommendations found.</div>';
            controls.innerHTML = '';
        }
    }
    renderPage(currentPage);
}

// --- Patch du chatbot pour affichage dynamique ---
document.addEventListener('DOMContentLoaded', function () {
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
            // ... code existant ...
            var response = await fetch('/cinema_chatbot_api', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ history: chatHistory })
            });
            var data = await response.json();
            // ... code existant ...
            // Mise à jour dynamique des recommandations dans Now Showing
            if (data.recommendations && data.recommendations.length) {
                updateNowShowing(data.recommendations);
            }
            // ... code existant ...
        });
    }
}); 