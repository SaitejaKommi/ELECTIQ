/**
 * Features module for ElectIQ.
 * Handles the Google Custom Search and Gemini Election Glossary UI logic.
 */

document.addEventListener('DOMContentLoaded', () => {
    initGlossary();
    initSearch();
});

/**
 * Initializes the Glossary feature event listeners.
 */
function initGlossary() {
    const glossaryForm = document.getElementById('glossary-form');
    const glossaryInput = document.getElementById('glossary-input');
    const glossaryResult = document.getElementById('glossary-result');
    
    if (!glossaryForm) return;

    glossaryForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const term = glossaryInput.value.trim();
        if (!term) return;

        // Log Google Analytics event
        if (typeof gtag === 'function') {
            gtag('event', 'glossary_search', {
                'event_category': 'Engagement',
                'event_label': term
            });
        }

        glossaryResult.classList.remove('hidden');
        glossaryResult.innerHTML = '<div class="spinner small"></div> Loading explanation...';
        
        try {
            const email = localStorage.getItem('electiq_user') || 'anonymous';
            const response = await fetch('/api/glossary/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ term: term, email: email })
            });
            
            const data = await response.json();
            if (response.ok) {
                glossaryResult.innerHTML = `<p><strong>${data.term}:</strong> ${data.explanation}</p>`;
            } else {
                glossaryResult.innerHTML = `<p class="error-text">Error: ${data.error || 'Failed to explain term'}</p>`;
            }
        } catch (error) {
            console.error('Glossary Error:', error);
            glossaryResult.innerHTML = `<p class="error-text">Network error. Please try again.</p>`;
        }
    });
}

/**
 * Initializes the Search feature event listeners.
 */
function initSearch() {
    const searchForm = document.getElementById('search-form');
    const searchInput = document.getElementById('search-input');
    const searchResults = document.getElementById('search-results');
    
    if (!searchForm) return;

    searchForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const query = searchInput.value.trim();
        if (!query) return;

        // Log Google Analytics event
        if (typeof gtag === 'function') {
            gtag('event', 'custom_search', {
                'event_category': 'Engagement',
                'event_label': query
            });
        }

        searchResults.innerHTML = '<div class="spinner small"></div> Loading results...';
        
        try {
            const response = await fetch(`/api/search/?q=${encodeURIComponent(query)}`);
            const data = await response.json();
            
            if (response.ok) {
                if (data.results && data.results.length > 0) {
                    let html = '<ul style="list-style: none; padding: 0;">';
                    data.results.forEach(item => {
                        html += `
                            <li style="margin-bottom: 10px; border-bottom: 1px solid var(--border-color); padding-bottom: 10px;">
                                <a href="${item.link}" target="_blank" rel="noopener noreferrer" style="font-weight: 600; color: var(--primary-color);">${item.title}</a>
                                <p style="font-size: 0.9em; margin: 5px 0 0 0;">${item.snippet}</p>
                            </li>
                        `;
                    });
                    html += '</ul>';
                    searchResults.innerHTML = html;
                } else {
                    searchResults.innerHTML = '<p>No results found.</p>';
                }
            } else {
                searchResults.innerHTML = `<p class="error-text">Error: ${data.error || 'Search failed'}</p>`;
            }
        } catch (error) {
            console.error('Search Error:', error);
            searchResults.innerHTML = `<p class="error-text">Network error. Please try again.</p>`;
        }
    });
}
