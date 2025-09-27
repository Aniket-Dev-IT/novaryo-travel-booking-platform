// Novaryo Main JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize Bootstrap tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize Bootstrap popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            alert.style.opacity = '0';
            setTimeout(function() {
                if (alert.parentNode) {
                    alert.parentNode.removeChild(alert);
                }
            }, 300);
        }, 5000);
    });

    // Form validation enhancement
    const forms = document.querySelectorAll('.needs-validation');
    forms.forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });

    // Loading button states
    const loadingButtons = document.querySelectorAll('[data-loading-text]');
    loadingButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            const originalText = button.textContent;
            const loadingText = button.dataset.loadingText;
            
            button.textContent = loadingText;
            button.disabled = true;
            button.classList.add('disabled');
            
            // Re-enable after form submission or timeout
            setTimeout(function() {
                button.textContent = originalText;
                button.disabled = false;
                button.classList.remove('disabled');
            }, 10000);
        });
    });

    // Confirm delete actions
    const deleteButtons = document.querySelectorAll('[data-confirm-delete]');
    deleteButtons.forEach(function(button) {
        button.addEventListener('click', function(event) {
            const confirmMessage = button.dataset.confirmDelete || 'Are you sure you want to delete this item?';
            if (!confirm(confirmMessage)) {
                event.preventDefault();
            }
        });
    });

    // Copy to clipboard functionality
    const copyButtons = document.querySelectorAll('[data-copy-target]');
    copyButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            const targetSelector = button.dataset.copyTarget;
            const target = document.querySelector(targetSelector);
            
            if (target) {
                const textToCopy = target.textContent || target.value;
                
                // Modern clipboard API
                if (navigator.clipboard) {
                    navigator.clipboard.writeText(textToCopy).then(function() {
                        showToast('Copied to clipboard!', 'success');
                    });
                } else {
                    // Fallback for older browsers
                    const textArea = document.createElement('textarea');
                    textArea.value = textToCopy;
                    document.body.appendChild(textArea);
                    textArea.select();
                    document.execCommand('copy');
                    document.body.removeChild(textArea);
                    showToast('Copied to clipboard!', 'success');
                }
            }
        });
    });

    // Dynamic form fields
    const addFieldButtons = document.querySelectorAll('[data-add-field]');
    addFieldButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            const templateSelector = button.dataset.addField;
            const template = document.querySelector(templateSelector);
            const container = document.querySelector(button.dataset.container);
            
            if (template && container) {
                const clone = template.cloneNode(true);
                clone.style.display = 'block';
                container.appendChild(clone);
            }
        });
    });

    // Remove field functionality
    document.addEventListener('click', function(event) {
        if (event.target.matches('[data-remove-field]')) {
            const fieldContainer = event.target.closest(event.target.dataset.removeField);
            if (fieldContainer) {
                fieldContainer.remove();
            }
        }
    });
});

// Utility Functions
function showToast(message, type = 'info') {
    const toastContainer = document.querySelector('#toast-container') || createToastContainer();
    
    const toast = document.createElement('div');
    toast.className = `toast align-items-center text-white bg-${type} border-0`;
    toast.setAttribute('role', 'alert');
    toast.setAttribute('aria-live', 'assertive');
    toast.setAttribute('aria-atomic', 'true');
    
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">${message}</div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>
    `;
    
    toastContainer.appendChild(toast);
    
    const bsToast = new bootstrap.Toast(toast);
    bsToast.show();
    
    // Remove toast element after it's hidden
    toast.addEventListener('hidden.bs.toast', function() {
        toast.remove();
    });
}

function createToastContainer() {
    const container = document.createElement('div');
    container.id = 'toast-container';
    container.className = 'toast-container position-fixed bottom-0 end-0 p-3';
    container.style.zIndex = '1055';
    document.body.appendChild(container);
    return container;
}

// API Helper Functions
async function apiRequest(url, options = {}) {
    const defaultOptions = {
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCsrfToken(),
        },
    };
    
    const finalOptions = Object.assign(defaultOptions, options);
    
    try {
        const response = await fetch(url, finalOptions);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('API request failed:', error);
        showToast('An error occurred. Please try again.', 'danger');
        throw error;
    }
}

function getCsrfToken() {
    const csrf = document.querySelector('[name=csrfmiddlewaretoken]');
    return csrf ? csrf.value : '';
}

// Loyalty Program Specific Functions
function updateLoyaltyPoints() {
    const pointsElements = document.querySelectorAll('[data-loyalty-points]');
    
    pointsElements.forEach(async function(element) {
        try {
            const response = await apiRequest('/api/loyalty/points/');
            element.textContent = response.points_balance.toLocaleString();
        } catch (error) {
            console.error('Failed to update loyalty points:', error);
        }
    });
}

// Auto-refresh loyalty points every 5 minutes
setInterval(updateLoyaltyPoints, 300000);

// Export functions for use in other scripts
window.NovaryoApp = {
    showToast,
    apiRequest,
    updateLoyaltyPoints,
    getCsrfToken
};