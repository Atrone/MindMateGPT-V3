function setViewState(state) {
    // Initially hide all divs
    document.getElementById("form").style.display = "none";
    document.getElementById("landing").style.display = "none";
    document.getElementById("chat").style.display = "none";
    document.getElementById("about").style.display = "none"; // New line for "info" div

    // Display the appropriate div based on the state
    if (state && state.view === 'form') {
        document.getElementById("form").style.display = "block";
    } else if (state && state.view === 'chat') {
        document.getElementById("chat").style.display = "block";
    } else if (state && state.view === 'about') { // New conditional for "info" div
        document.getElementById("about").style.display = "block";
    } else {
        document.getElementById("landing").style.display = "block";
    }
}

// Originally your hideContent function
function hideContent() {
    history.pushState({ view: 'form' }, '', '');
    setViewState({ view: 'form' });
}

function showChat() {
    // Push landing onto the history to ensure that going back from chat returns to landing
    history.pushState({ view: 'landing' }, '', '');
    history.pushState({ view: 'chat' }, '', '');
    setViewState({ view: 'chat' });
}

function showInfo() {
    history.pushState({ view: 'about' }, '', '');
    setViewState({ view: 'about' });
}

// This will handle the popstate event
window.addEventListener('popstate', function(event) {
    setViewState(event.state);
});

// Push an initial state to represent the landing view when the page loads
window.addEventListener('load', function() {
    history.replaceState({ view: 'landing' }, '', '');
});

