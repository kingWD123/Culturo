// Restaurant Page JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Handle button hover effects
    const getRecommendationBtn = document.querySelector('.btn-get-recommendation');
    
    if (getRecommendationBtn) {
        getRecommendationBtn.addEventListener('mouseenter', function() {
            this.style.backgroundColor = '#c70812';
            this.style.transform = 'scale(1.05)';
            this.style.boxShadow = '0 6px 12px rgba(230, 9, 20, 0.5)';
        });
        
        getRecommendationBtn.addEventListener('mouseleave', function() {
            this.style.backgroundColor = '#e60914';
            this.style.transform = 'scale(1)';
            this.style.boxShadow = '0 4px 8px rgba(230, 9, 20, 0.3)';
        });
    }
});