window.initNews = async function() {
    const container = document.getElementById('news-container');
    
    try {
        const response = await fetch('/api/news/');
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
        container.innerHTML = '<p class="error-text">Unable to load news at this time.</p>';
    }
};
