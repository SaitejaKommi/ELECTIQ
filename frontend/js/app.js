document.addEventListener('DOMContentLoaded', () => {
    // Theme toggler
    const themeToggle = document.getElementById('theme-toggle');
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

    // Language selector
    const langSelect = document.getElementById('language-selector');
    langSelect.addEventListener('change', (e) => {
        setLanguage(e.target.value);
        // Re-render dynamic components
        if (window.initTimeline) window.initTimeline();
        if (window.initChecklist) window.initChecklist();
        if (window.initNews) window.initNews();
    });

    // Tab switcher
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
            document.getElementById(`${target}-section`).classList.remove('hidden');
        });
    });
});
