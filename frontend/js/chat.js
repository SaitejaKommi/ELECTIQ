document.addEventListener('DOMContentLoaded', () => {
    const chatForm = document.getElementById('chat-form');
    const chatInput = document.getElementById('chat-input');
    const chatHistory = document.getElementById('chat-history');

    let debounceTimer;

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

    async function sendMessage(message) {
        const email = getUserEmail();
        if (!email) return;

        // Add user message to UI
        addMessageToUI('user', message);
        
        // Add loading indicator
        const loadingId = 'loading-' + Date.now();
        addMessageToUI('model', '<div class="spinner" style="width:20px;height:20px;margin:0;"></div>', loadingId);

        try {
            const response = await fetch('/api/chat/', {
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

    function addMessageToUI(role, htmlContent, id = null) {
        const msgDiv = document.createElement('div');
        msgDiv.className = `message ${role}`;
        if (id) msgDiv.id = id;
        
        // If it's a model response (and not loading), add a TTS button
        if (role === 'model' && !htmlContent.includes('spinner')) {
            msgDiv.innerHTML = `
                <div>${htmlContent}</div>
                <button class="tts-btn" aria-label="Listen" onclick="playTTS(this.previousElementSibling.innerText)">🔊</button>
            `;
        } else {
            msgDiv.innerHTML = `<div>${htmlContent}</div>`;
        }
        
        chatHistory.appendChild(msgDiv);
        chatHistory.scrollTop = chatHistory.scrollHeight;
    }

    function formatResponse(text) {
        // Very basic markdown parsing for bold text
        return text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
                   .replace(/\n/g, '<br>');
    }
});

let synth = window.speechSynthesis;
let currentUtterance = null;

async function playTTS(text) {
    if (synth.speaking) {
        synth.cancel();
        return; // act as a toggle
    }
    
    if (text !== '') {
        currentUtterance = new SpeechSynthesisUtterance(text);
        currentUtterance.lang = currentLanguage === 'en' ? 'en-US' : (currentLanguage + '-' + currentLanguage.toUpperCase());
        synth.speak(currentUtterance);
    }
}
