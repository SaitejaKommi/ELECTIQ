/**
 * Application state for the quiz module.
 */
let quizData = [];
let currentQuestionIndex = 0;
let score = 0;

document.addEventListener('DOMContentLoaded', () => {
    const startBtn = document.getElementById('start-quiz-btn');
    const restartBtn = document.getElementById('restart-quiz-btn');
    const nextBtn = document.getElementById('next-q-btn');
    
    startBtn?.addEventListener('click', startQuiz);
    restartBtn?.addEventListener('click', startQuiz);
    nextBtn?.addEventListener('click', loadNextQuestion);
});

/**
 * Initializes and starts a new quiz session.
 * Fetches quiz data from the backend and resets the UI state.
 */
async function startQuiz() {
    // Log Google Analytics event
    if (typeof gtag === 'function') {
        gtag('event', 'quiz_started', {
            'event_category': 'Engagement'
        });
    }

    document.getElementById('quiz-intro').classList.add('hidden');
    document.getElementById('quiz-results').classList.add('hidden');
    
    const container = document.getElementById('quiz-container');
    container.classList.remove('hidden');
    container.innerHTML = '<div class="spinner" aria-label="Loading quiz"></div><p style="text-align:center;">Generating quiz...</p>';
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/quiz/`);
        if (!response.ok) throw new Error("Failed to fetch quiz");
        
        quizData = await response.json();
        
        // Restore container structure
        container.innerHTML = `
            <div id="quiz-progress" aria-atomic="true">Question <span id="q-num">1</span> of ${quizData.length}</div>
            <h3 id="quiz-question"></h3>
            <div id="quiz-options" class="quiz-options" role="radiogroup" aria-labelledby="quiz-question"></div>
            <div id="quiz-feedback" class="hidden" role="alert"></div>
            <button id="next-q-btn" class="btn primary hidden" aria-label="Next Question">Next Question</button>
        `;
        
        document.getElementById('next-q-btn').addEventListener('click', loadNextQuestion);
        
        currentQuestionIndex = 0;
        score = 0;
        
        if (quizData && quizData.length > 0) {
            await renderQuestion();
        } else {
            throw new Error("Empty quiz data");
        }
    } catch (error) {
        console.error(error);
        container.innerHTML = '<p class="error-text" role="alert">Failed to load quiz. Please try again.</p><button onclick="startQuiz()" class="btn outline">Retry</button>';
    }
}

/**
 * Renders the current question and its options.
 * Handles translations of the question and options.
 */
async function renderQuestion() {
    const q = quizData[currentQuestionIndex];
    
    document.getElementById('q-num').textContent = currentQuestionIndex + 1;
    
    const transQ = await translateDynamicText(q.question, currentLanguage);
    document.getElementById('quiz-question').textContent = transQ;
    
    const optionsContainer = document.getElementById('quiz-options');
    optionsContainer.innerHTML = '';
    
    const feedback = document.getElementById('quiz-feedback');
    feedback.classList.add('hidden');
    feedback.className = '';
    
    document.getElementById('next-q-btn').classList.add('hidden');
    
    for (let i = 0; i < q.options.length; i++) {
        const transOpt = await translateDynamicText(q.options[i], currentLanguage);
        const btn = document.createElement('button');
        btn.className = 'quiz-option';
        btn.setAttribute('role', 'radio');
        btn.setAttribute('aria-checked', 'false');
        btn.textContent = transOpt;
        btn.onclick = () => handleAnswer(i, btn);
        optionsContainer.appendChild(btn);
    }
}

/**
 * Evaluates the user's selected answer and displays feedback.
 * @param {number} selectedIndex - The index of the selected option.
 * @param {HTMLElement} btnElement - The button element that was clicked.
 */
async function handleAnswer(selectedIndex, btnElement) {
    // Disable all options
    const options = document.querySelectorAll('.quiz-option');
    options.forEach(opt => opt.disabled = true);
    
    btnElement.setAttribute('aria-checked', 'true');
    
    const q = quizData[currentQuestionIndex];
    const isCorrect = selectedIndex === q.correct_index;
    
    if (isCorrect) {
        score++;
        btnElement.classList.add('correct');
    } else {
        btnElement.classList.add('incorrect');
        options[q.correct_index].classList.add('correct');
    }
    
    const feedback = document.getElementById('quiz-feedback');
    const transExpl = await translateDynamicText(q.explanation, currentLanguage);
    feedback.textContent = transExpl;
    feedback.classList.remove('hidden');
    feedback.classList.add(isCorrect ? 'success' : 'error');
    
    document.getElementById('next-q-btn').classList.remove('hidden');
}

/**
 * Advances to the next question or shows the final results.
 */
async function loadNextQuestion() {
    currentQuestionIndex++;
    if (currentQuestionIndex < quizData.length) {
        await renderQuestion();
    } else {
        showResults();
    }
}

/**
 * Displays the final score and saves it to the backend database.
 */
async function showResults() {
    document.getElementById('quiz-container').classList.add('hidden');
    document.getElementById('quiz-results').classList.remove('hidden');
    document.getElementById('final-score').textContent = score;
    
    // Log Google Analytics event
    if (typeof gtag === 'function') {
        gtag('event', 'quiz_completed', {
            'event_category': 'Engagement',
            'value': score
        });
    }

    // Save score to DB
    const email = getUserEmail();
    if (email) {
        try {
            await fetch(`${API_BASE_URL}/api/quiz/score`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, score, total: quizData.length })
            });
        } catch (e) {
            console.error("Failed to save score");
        }
    }
}
