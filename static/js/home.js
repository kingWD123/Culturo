// Apparition douce avec stagger section par section
function revealOnScroll() {
    document.querySelectorAll('.section, .decouvertes, .univers-grid, .decouvertes-grid').forEach(section => {
        const cards = section.querySelectorAll('.reveal');
        const windowHeight = window.innerHeight;
        let anyVisible = false;
        cards.forEach((el, idx) => {
            const elementTop = el.getBoundingClientRect().top;
            if (elementTop < windowHeight - 60) {
                setTimeout(() => el.classList.add('active'), idx * 60);
                anyVisible = true;
            } else {
                el.classList.remove('active');
            }
        });
    });
}

function createRipple(e) {
    const btn = e.currentTarget;
    const circle = document.createElement('span');
    const diameter = Math.max(btn.clientWidth, btn.clientHeight);
    const radius = diameter / 2;
    circle.style.width = circle.style.height = `${diameter}px`;
    circle.style.left = `${e.clientX - btn.getBoundingClientRect().left - radius}px`;
    circle.style.top = `${e.clientY - btn.getBoundingClientRect().top - radius}px`;
    circle.classList.add('ripple');
    btn.appendChild(circle);
    setTimeout(() => circle.remove(), 600);
}

function tiltCard(card) {
    card.addEventListener('mousemove', e => {
        const rect = card.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        const centerX = rect.width / 2;
        const centerY = rect.height / 2;
        const rotateX = ((y - centerY) / centerY) * 6;
        const rotateY = ((x - centerX) / centerX) * 6;
        card.style.transform = `rotateX(${-rotateX}deg) rotateY(${rotateY}deg)`;
        card.style.transition = 'transform 0.1s';
    });
    card.addEventListener('mouseleave', () => {
        card.style.transform = '';
        card.style.transition = 'transform 0.4s cubic-bezier(.4,2,.3,1)';
    });
}

function animateCounter(el, to) {
    let start = 0;
    const duration = 1200;
    const step = Math.ceil(to / (duration / 16));
    function update() {
        start += step;
        if (start >= to) {
            el.textContent = to;
        } else {
            el.textContent = start;
            requestAnimationFrame(update);
        }
    }
    update();
}

document.addEventListener('DOMContentLoaded', function () {
    // Apparition douce
    revealOnScroll();
    window.addEventListener('scroll', revealOnScroll);

    // Ajout automatique de la classe .reveal sur les cards
    document.querySelectorAll('.univers-card, .decouverte-card, .testimonial-content, .newsletter').forEach(el => {
        el.classList.add('reveal');
    });

    // Effet zoom/ombre sur images (rebond JS)
    document.querySelectorAll('.hero-image img, .univers-card img, .decouverte-card img').forEach(img => {
        img.addEventListener('mouseenter', () => {
            img.style.transform = 'scale(1.06)';
            img.style.transition = 'transform 0.3s cubic-bezier(.4,2,.3,1)';
        });
        img.addEventListener('mouseleave', () => {
            img.style.transform = 'scale(1)';
        });
    });

    // Bouton scroll-to-top
    const scrollBtn = document.createElement('button');
    scrollBtn.innerHTML = '↑';
    scrollBtn.setAttribute('aria-label', 'Remonter');
    scrollBtn.style.position = 'fixed';
    scrollBtn.style.bottom = '32px';
    scrollBtn.style.right = '32px';
    scrollBtn.style.background = '#ff6b35';
    scrollBtn.style.color = 'white';
    scrollBtn.style.border = 'none';
    scrollBtn.style.borderRadius = '50%';
    scrollBtn.style.width = '48px';
    scrollBtn.style.height = '48px';
    scrollBtn.style.fontSize = '1.7rem';
    scrollBtn.style.boxShadow = '0 4px 20px rgba(255,107,53,0.25)';
    scrollBtn.style.cursor = 'pointer';
    scrollBtn.style.opacity = '0';
    scrollBtn.style.pointerEvents = 'none';
    scrollBtn.style.transition = 'opacity 0.3s';
    document.body.appendChild(scrollBtn);
    window.addEventListener('scroll', () => {
        if (window.scrollY > 300) {
            scrollBtn.style.opacity = '1';
            scrollBtn.style.pointerEvents = 'auto';
        } else {
            scrollBtn.style.opacity = '0';
            scrollBtn.style.pointerEvents = 'none';
        }
    });
    scrollBtn.addEventListener('click', () => {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });

    // Parallax sur le watermark du hero
    const watermark = document.querySelector('.hero img[alt="Carte du monde"]');
    if (watermark) {
        window.addEventListener('scroll', () => {
            const scrolled = window.scrollY;
            watermark.style.transform = `translateY(${scrolled * 0.08}px)`;
        });
    }

    // Effet ripple sur les boutons principaux
    document.querySelectorAll('.cta-button, .header-cta, .newsletter-form button, .view-all').forEach(btn => {
        btn.style.position = 'relative';
        btn.style.overflow = 'hidden';
        btn.addEventListener('click', createRipple);
    });

    // Tilt 3D sur les cartes univers/découvertes
    document.querySelectorAll('.univers-card, .decouverte-card').forEach(tiltCard);

    // Focus animé sur le champ email de la newsletter
    const emailInput = document.querySelector('.newsletter-form input[type="email"]');
    if (emailInput) {
        emailInput.addEventListener('focus', () => {
            emailInput.style.boxShadow = '0 0 0 3px #ff6b3533';
            emailInput.style.transition = 'box-shadow 0.3s';
        });
        emailInput.addEventListener('blur', () => {
            emailInput.style.boxShadow = '';
        });
    }

    // Animation de compteur sur un chiffre clé (ex: univers explorés)
    const counter = document.querySelector('.counter-animated');
    if (counter) {
        let done = false;
        function onScroll() {
            const rect = counter.getBoundingClientRect();
            if (!done && rect.top < window.innerHeight) {
                animateCounter(counter, parseInt(counter.dataset.to, 10));
                done = true;
            }
        }
        window.addEventListener('scroll', onScroll);
        window.addEventListener('DOMContentLoaded', onScroll);
    }

    // Effet 3D tilt/parallax sur les images du hero (desktop uniquement)
    const heroImages = document.querySelectorAll('.hero-image');
    const heroImagesContainer = document.querySelector('.hero-images');
    if (heroImages.length && heroImagesContainer && window.innerWidth > 768) {
        heroImagesContainer.addEventListener('mousemove', e => {
            const rect = heroImagesContainer.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;
            heroImages.forEach((img, i) => {
                const intensity = i === 1 ? 1.2 : 0.7; // image large = plus d'effet
                const rotateX = ((y - centerY) / centerY) * 7 * intensity;
                const rotateY = ((x - centerX) / centerX) * 7 * intensity;
                img.style.transform = `rotateX(${-rotateX}deg) rotateY(${rotateY}deg)`;
            });
        });
        heroImagesContainer.addEventListener('mouseleave', () => {
            heroImages.forEach(img => {
                img.style.transform = '';
            });
        });
    }
}); 