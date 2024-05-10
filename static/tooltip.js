// Variable for delay in milliseconds
const DELAY = 2000;

// Function to enable tooltips
/**
 * Enables tooltips by selecting all elements with 'data-bs-toggle="tooltip"' attribute
 * and initializing Bootstrap tooltips for each element.
 * Attaches a event listener to each tooltip element to hide after 2 seconds.
 */
function enableTooltips() {
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => {
        const tooltipInstance = new bootstrap.Tooltip(tooltipTriggerEl);
        tooltipTriggerEl.addEventListener('show.bs.tooltip', () => {
            setTimeout(() => tooltipInstance.hide(), DELAY);             
        });
        return tooltipInstance;
    });
}


// Enable tooltips
enableTooltips();