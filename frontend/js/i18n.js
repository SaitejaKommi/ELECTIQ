/**
 * Dictionary for static UI translations.
 * @type {Object<string, Object<string, string>>}
 */
const i18nDictionary = {
    en: {
        chat_heading: "AI Election Assistant",
        timeline_heading: "Election Timeline",
        news_heading: "Latest Election News",
        quiz_desc: "Test your knowledge with our 10-question quiz!",
        quiz_complete: "Quiz Complete!"
    },
    hi: {
        chat_heading: "एआई चुनाव सहायक",
        timeline_heading: "चुनाव समयरेखा",
        news_heading: "नवीनतम चुनाव समाचार",
        quiz_desc: "हमारे 10-प्रश्नों की प्रश्नोत्तरी के साथ अपने ज्ञान का परीक्षण करें!",
        quiz_complete: "प्रश्नोत्तरी पूर्ण!"
    },
    es: {
        chat_heading: "Asistente Electoral de IA",
        timeline_heading: "Cronograma Electoral",
        news_heading: "Últimas Noticias Electorales",
        quiz_desc: "¡Pon a prueba tus conocimientos con nuestro cuestionario de 10 preguntas!",
        quiz_complete: "¡Cuestionario Completo!"
    },
    fr: {
        chat_heading: "Assistant Électoral IA",
        timeline_heading: "Calendrier Électoral",
        news_heading: "Dernières Nouvelles Électorales",
        quiz_desc: "Testez vos connaissances avec notre quiz de 10 questions!",
        quiz_complete: "Quiz Terminé!"
    },
    te: {
        chat_heading: "AI ఎన్నికల సహాయకుడు",
        timeline_heading: "ఎన్నికల కాలక్రమం",
        news_heading: "తాజా ఎన్నికల వార్తలు",
        quiz_desc: "మా 10-ప్రశ్నల క్విజ్‌తో మీ జ్ఞానాన్ని పరీక్షించుకోండి!",
        quiz_complete: "క్విజ్ పూర్తయింది!"
    }
};

/** @type {string} */
let currentLanguage = 'en';

/**
 * Memory cache for dynamic translations to minimize redundant API calls.
 * @type {Map<string, string>}
 */
const translationCache = new Map();

/**
 * Updates the static UI elements with translated strings from the dictionary.
 * @param {string} lang - Target language code (e.g., 'es').
 */
function setLanguage(lang) {
    if (!i18nDictionary[lang]) return;
    currentLanguage = lang;
    
    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');
        if (i18nDictionary[lang][key]) {
            el.textContent = i18nDictionary[lang][key];
        }
    });
}

/**
 * Translates dynamic content using the backend API.
 * Uses a JS Map to cache translations and minimize redundant API calls.
 * @param {string} text - Original text to translate.
 * @param {string} targetLang - Target language code.
 * @returns {Promise<string>} Translated text.
 */
async function translateDynamicText(text, targetLang) {
    if (targetLang === 'en' || !text) return text;
    
    const cacheKey = `${targetLang}_${text}`;
    if (translationCache.has(cacheKey)) {
        return translationCache.get(cacheKey);
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/translate/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text, target_language: targetLang })
        });
        
        if (!response.ok) throw new Error("Translation failed");
        
        const data = await response.json();
        translationCache.set(cacheKey, data.translatedText);
        return data.translatedText;
    } catch (error) {
        console.error(error);
        return text; // fallback to original
    }
}
