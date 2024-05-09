// Function to enable tooltips
/**
 * Enables tooltips by selecting all elements with 'data-bs-toggle="tooltip"' attribute
 * and initializing Bootstrap tooltips for each element.
 */
function enableTooltips() {
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));
}


// Enable tooltips
enableTooltips();