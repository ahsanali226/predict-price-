// EstateAI - Main Script
document.addEventListener('DOMContentLoaded', () => {
    const inputs = document.querySelectorAll('input');
    const form = document.querySelector('form');
    const button = document.querySelector('.btn-predict');

    // Input focus effect
    inputs.forEach(input => {
        input.addEventListener('focus', () => {
            const formGroup = input.closest('.form-group');
            if (formGroup) {
                formGroup.style.transform = 'scale(1.02)';
                formGroup.style.transition = 'all 0.3s ease';
            }
        });

        input.addEventListener('blur', () => {
            const formGroup = input.closest('.form-group');
            if (formGroup) {
                formGroup.style.transform = 'scale(1)';
            }
        });

        // Real-time validation feedback
        input.addEventListener('input', () => {
            validateInput(input);
        });
    });

    // Form submission
    form.addEventListener('submit', (e) => {
        // Validate all inputs before submission
        let isValid = true;
        inputs.forEach(input => {
            if (!validateInput(input)) {
                isValid = false;
            }
        });

        if (!isValid) {
            e.preventDefault();
            showNotification('Please fix the errors above', 'error');
            return;
        }

        // Show loading state
        button.innerHTML = '<span class="loader">Calculating...</span>';
        button.style.opacity = '0.8';
        button.disabled = true;
    });
});

/**
 * Validate individual input
 */
function validateInput(input) {
    const value = input.value.trim();
    const min = parseInt(input.getAttribute('min'));
    const max = parseInt(input.getAttribute('max'));
    let isValid = true;

    // Clear previous error
    const error = input.parentElement.querySelector('.error-message');
    if (error) {
        error.remove();
    }

    if (value === '') {
        return true; // Empty is OK (HTML required will catch it)
    }

    const numValue = parseFloat(value);

    if (isNaN(numValue)) {
        showInputError(input, 'Please enter a valid number');
        isValid = false;
    } else if (numValue < min) {
        showInputError(input, `Minimum value is ${min}`);
        isValid = false;
    } else if (numValue > max) {
        showInputError(input, `Maximum value is ${max}`);
        isValid = false;
    } else if (input.name === 'square_feet' && numValue === 0) {
        showInputError(input, 'Area must be greater than 0');
        isValid = false;
    }

    return isValid;
}

/**
 * Show input error message
 */
function showInputError(input, message) {
    const error = document.createElement('span');
    error.className = 'error-message';
    error.textContent = '⚠ ' + message;
    error.style.cssText = `
        display: block;
        color: #ff6b6b;
        font-size: 0.75rem;
        margin-top: 4px;
        padding-left: 4px;
    `;

    // Remove existing error
    const existingError = input.parentElement.querySelector('.error-message');
    if (existingError) {
        existingError.remove();
    }

    input.parentElement.appendChild(error);
    input.style.borderColor = '#e74c3c';
}

/**
 * Show notification
 */
function showNotification(message, type = 'info') {
    console.log(`[${type.toUpperCase()}] ${message}`);
}

/**
 * Clear form
 */
function clearForm() {
    document.querySelectorAll('input').forEach(input => {
        input.value = '';
        input.style.borderColor = '';
        const error = input.parentElement.querySelector('.error-message');
        if (error) {
            error.remove();
        }
    });
}

// Keyboard shortcuts
document.addEventListener('keydown', (e) => {
    // Enter key to submit form
    if (e.key === 'Enter' && e.ctrlKey) {
        const form = document.querySelector('form');
        form.dispatchEvent(new Event('submit'));
    }
});
