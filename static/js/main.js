// EstateAI - Main Script
document.addEventListener('DOMContentLoaded', () => {
    const inputs = document.querySelectorAll('input');
    
    inputs.forEach(input => {
        // Add subtle focus effect on container
        input.addEventListener('focus', () => {
            input.parentElement.parentElement.style.transform = 'scale(1.02)';
            input.parentElement.parentElement.style.transition = 'all 0.3s ease';
        });
        
        input.addEventListener('blur', () => {
            input.parentElement.parentElement.style.transform = 'scale(1)';
        });
    });

    // Handle form submission animation if needed
    const form = document.querySelector('form');
    const button = document.querySelector('.btn-predict');

    form.addEventListener('submit', () => {
        button.innerHTML = '<span class="loader">Calculating...</span>';
        button.style.opacity = '0.8';
        button.disabled = true;
    });
});
