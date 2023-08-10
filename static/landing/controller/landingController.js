// This function will handle the display of the divs based on the provided state
function setViewState(state) {
    if (state && state.view === 'form') {
        document.getElementById("form").style.display = "block";
        document.getElementById("landing").style.display = "none";
    } else {
        document.getElementById("form").style.display = "none";
        document.getElementById("landing").style.display = "block";
    }
}

function hideContent() {
    document.getElementById("form").style.display = "block";
    document.getElementById("landing").style.display = "none";

    // Push a new state to represent the form view
    history.pushState({ view: 'form' }, '', '');
}

// This will handle the popstate event
window.addEventListener('popstate', function(event) {
    setViewState(event.state);
});

// Push an initial state to represent the landing view when the page loads
window.addEventListener('load', function() {
    history.replaceState({ view: 'landing' }, '', '');
});
