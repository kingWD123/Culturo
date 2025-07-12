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