/**
 * Initializes the news section by fetching articles from the backend.
 * Uses IntersectionObserver to implement lazy loading.
 */
window.initNews = async function() {
    const container = document.getElementById('news-container');
    const newsSection = document.querySelector('.news-section');
    
    let isNewsLoaded = false;
    
    /**
     * Observer callback to fetch news only when the section is visible.
     * @param {IntersectionObserverEntry[]} entries - Observation entries.
     */
    const loadNewsOnScroll = async (entries) => {
        const [entry] = entries;
        if (entry.isIntersecting && !isNewsLoaded) {
            isNewsLoaded = true;
            await fetchNews(container);
            observer.unobserve(newsSection);
        }
    };

    const observer = new IntersectionObserver(loadNewsOnScroll, { threshold: 0.1 });
    if (newsSection) {
        observer.observe(newsSection);
    }
};

/**
 * Helper function to fetch and render news articles.
 * @param {HTMLElement} container - DOM element to render news into.
 */
async function fetchNews(container) {
    try {
        const response = await fetch(`${API_BASE_URL}/api/news/`);
        if (!response.ok) throw new Error('Failed to fetch news');
        
        const articles = await response.json();
        container.innerHTML = '';
        
        if (articles.length === 0) {
            container.innerHTML = '<p>No recent news found.</p>';
            return;
        }
        
        for (const article of articles) {
            const transTitle = await translateDynamicText(article.title, currentLanguage);
            const transSnippet = await translateDynamicText(article.snippet, currentLanguage);
            
            const card = document.createElement('div');
            card.className = 'news-card';
            card.innerHTML = `
                <a href="${article.link}" target="_blank" rel="noopener noreferrer">${transTitle}</a>
                <p>${transSnippet}</p>
            `;
            container.appendChild(card);
        }
    } catch (error) {
        console.error(error);
        container.innerHTML = '<p class="error-text" role="alert">Unable to load news at this time.</p>';
    }
}
