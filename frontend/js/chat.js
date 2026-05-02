/**
 * Main chat interface module.
 * Handles user interactions, message sending, debouncing,
 * and text-to-speech functionality.
 */
document.addEventListener('DOMContentLoaded', () => {
    const chatForm = document.getElementById('chat-form');
    const chatInput = document.getElementById('chat-input');
    const chatHistory = document.getElementById('chat-history');

    /** @type {number} Timer for debouncing chat inputs */
    let debounceTimer;

    /**
     * Handles the chat form submission with a debounce to prevent spam.
     * @param {Event} e - Form submit event
     */
    chatForm.addEventListener('submit', (e) => {
        e.preventDefault();
        
        // Debounce protection
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(() => {
            const message = chatInput.value.trim();
            if (message) {
                sendMessage(message);
                chatInput.value = '';
            }
        }, 300);
    });

    /**
     * Sends the user's message to the backend and updates the UI.
     * Handles translation of the AI response if a different language is selected.
     * @param {string} message - User's chat message
     */
    async function sendMessage(message) {
        const email = getUserEmail();
        if (!email) return;

        // Log Google Analytics event
        if (typeof gtag === 'function') {
            gtag('event', 'chat_message_sent', {
                'event_category': 'Engagement'
            });
        }

        // Add user message to UI
        addMessageToUI('user', message);
        
        // Add loading indicator
        const loadingId = 'loading-' + Date.now();
        addMessageToUI('model', '<div class="spinner small" style="width:20px;height:20px;margin:0;" aria-label="Loading response"></div>', loadingId);

        try {
            const response = await fetch(`${API_BASE_URL}/api/chat/`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, message })
            });
            
            const data = await response.json();
            
            // Remove loading
            document.getElementById(loadingId)?.remove();
            
            if (response.ok) {
                // Translate response if needed
                const finalResponse = await translateDynamicText(data.response, currentLanguage);
                addMessageToUI('model', formatResponse(finalResponse));
            } else {
                addMessageToUI('model', 'Sorry, I encountered an error: ' + (data.error || "Unknown error"));
            }
        } catch (error) {
            document.getElementById(loadingId)?.remove();
            addMessageToUI('model', 'Network error. Please try again.');
        }
    }

    /**
     * Appends a new message element to the chat history.
     * @param {string} role - 'user' or 'model'
     * @param {string} htmlContent - Formatted HTML content
     * @param {string|null} [id=null] - Optional element ID
     */
    function addMessageToUI(role, htmlContent, id = null) {
        const msgDiv = document.createElement('div');
        msgDiv.className = `message ${role}`;
        if (id) msgDiv.id = id;
        
        // If it's a model response (and not loading), add a TTS button
        if (role === 'model' && !htmlContent.includes('spinner')) {
            msgDiv.innerHTML = `
                <div>${htmlContent}</div>
                <button class="tts-btn" aria-label="Listen to this message" onclick="playTTS(this.previousElementSibling.innerText)">🔊</button>
            `;
        } else {
            msgDiv.innerHTML = `<div>${htmlContent}</div>`;
        }
        
        chatHistory.appendChild(msgDiv);
        chatHistory.scrollTop = chatHistory.scrollHeight;
    }

    /**
     * Formats basic markdown in the AI response into HTML.
     * @param {string} text - Raw text from AI
     * @returns {string} HTML formatted string
     */
    function formatResponse(text) {
        return text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
                   .replace(/\n/g, '<br>');
    }
});

let synth = window.speechSynthesis;
let currentUtterance = null;
let currentAudio = null;

/**
 * Uses Google Cloud TTS via backend, falls back to Web Speech API.
 * Acts as a toggle (cancels speaking if already speaking).
 * @param {string} text - The text to speak.
 */
async function playTTS(text) {
    // Check if audio is playing from Google TTS
    if (currentAudio && !currentAudio.paused) {
        currentAudio.pause();
        return;
    }
    
    // Check if speaking from Web Speech API
    if (synth.speaking) {
        synth.cancel();
        return;
    }
    
    if (!text) return;
    
    try {
        const response = await fetch('/api/tts/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text, language_code: currentLanguage })
        });
        
        const data = await response.json();
        if (response.ok && data.audioContent) {
            // Play Google TTS audio
            const audioSrc = 'data:audio/mp3;base64,' + data.audioContent;
            currentAudio = new Audio(audioSrc);
            currentAudio.play();
            return;
        }
    } catch (e) {
        console.warn("Google TTS failed, falling back to Web Speech API", e);
    }
    
    // Fallback to Web Speech API
    currentUtterance = new SpeechSynthesisUtterance(text);
    currentUtterance.lang = currentLanguage === 'en' ? 'en-US' : (currentLanguage + '-' + currentLanguage.toUpperCase());
    synth.speak(currentUtterance);
}
