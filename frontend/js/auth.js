document.addEventListener('DOMContentLoaded', () => {
    const loginOverlay = document.getElementById('login-overlay');
    const appContainer = document.getElementById('app-container');
    const loginForm = document.getElementById('login-form');
    const emailInput = document.getElementById('email-input');
    const loginError = document.getElementById('login-error');
    const userEmailDisplay = document.getElementById('user-email-display');
    const logoutBtn = document.getElementById('logout-btn');

    // Check if user is already logged in
    const storedEmail = sessionStorage.getItem('userEmail');
    if (storedEmail) {
        completeLogin(storedEmail);
    }

    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const email = emailInput.value.trim();
        
        try {
            const response = await fetch('/api/auth/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email })
            });
            
            const data = await response.json();
            
            if (response.ok) {
                sessionStorage.setItem('userEmail', data.email);
                completeLogin(data.email);
            } else {
                loginError.textContent = data.error || "Login failed";
                loginError.classList.remove('hidden');
            }
        } catch (error) {
            loginError.textContent = "Network error. Is the server running?";
            loginError.classList.remove('hidden');
        }
    });

    logoutBtn.addEventListener('click', () => {
        sessionStorage.removeItem('userEmail');
        location.reload(); // Reload to reset state
    });

    function completeLogin(email) {
        loginOverlay.classList.remove('active');
        loginOverlay.classList.add('hidden');
        appContainer.classList.remove('hidden');
        userEmailDisplay.textContent = email;
        
        // Initialize other modules
        if (window.initNews) window.initNews();
        if (window.initTimeline) window.initTimeline();
        if (window.initChecklist) window.initChecklist();
    }
});

function getUserEmail() {
    return sessionStorage.getItem('userEmail');
}
