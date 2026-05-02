/**
 * Main application initialization and event binding.
 * Sets up theme toggling, language selection, and tab switching.
 * Fetches the Election Fact of the Day on load.
 */
document.addEventListener('DOMContentLoaded', () => {
    initThemeToggle();
    initLanguageSelector();
    initTabSwitcher();
    fetchFactOfTheDay();
});

/**
 * Initializes the dark mode toggle functionality.
 */
function initThemeToggle() {
    const themeToggle = document.getElementById('theme-toggle');
    if (!themeToggle) return;
    
    themeToggle.addEventListener('click', () => {
        const body = document.body;
        const currentTheme = body.getAttribute('data-theme');
        if (currentTheme === 'dark') {
            body.removeAttribute('data-theme');
            themeToggle.textContent = '🌙';
        } else {
            body.setAttribute('data-theme', 'dark');
            themeToggle.textContent = '☀️';
        }
    });
}

/**
 * Initializes the language selection dropdown.
 */
function initLanguageSelector() {
    const langSelect = document.getElementById('language-selector');
    if (!langSelect) return;
    
    langSelect.addEventListener('change', (e) => {
        setLanguage(e.target.value);
        // Re-render dynamic components
        if (window.initTimeline) window.initTimeline();
        if (window.initChecklist) window.initChecklist();
        if (window.initNews) window.initNews();
        fetchFactOfTheDay(); // Re-translate fact
    });
}

/**
 * Initializes the tab switching logic between Checklist and Quiz.
 */
function initTabSwitcher() {
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            // Remove active classes
            tabBtns.forEach(b => {
                b.classList.remove('active');
                b.setAttribute('aria-selected', 'false');
            });
            tabContents.forEach(c => c.classList.add('hidden'));

            // Add active class to clicked tab
            btn.classList.add('active');
            btn.setAttribute('aria-selected', 'true');
            const target = btn.getAttribute('data-target');
            const targetSection = document.getElementById(`${target}-section`);
            if (targetSection) targetSection.classList.remove('hidden');
        });
    });
}

/**
 * Fetches the Election Fact of the Day from the backend and renders it.
 */
async function fetchFactOfTheDay() {
    const factContainer = document.getElementById('fact-of-the-day');
    if (!factContainer) return;
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/fact/`);
        if (!response.ok) throw new Error('Failed to fetch fact');
        
        const data = await response.json();
        const translatedFact = await translateDynamicText(data.fact, currentLanguage);
        
        factContainer.innerHTML = `<strong>💡 Fact of the Day:</strong> ${translatedFact}`;
        factContainer.setAttribute('aria-busy', 'false');
    } catch (error) {
        console.error(error);
        factContainer.innerHTML = `<strong>💡 Fact of the Day:</strong> Your voice matters! Register to vote today.`;
        factContainer.setAttribute('aria-busy', 'false');
    }
}

