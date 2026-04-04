const API_BASE = '';

const promptInput = document.getElementById('promptInput');
const charCount = document.getElementById('charCount');
const forgeBtn = document.getElementById('forgeBtn');
const statusIndicator = document.getElementById('statusIndicator');
const resultSection = document.getElementById('resultSection');
const placeholder = document.getElementById('placeholder');
const imageContainer = document.getElementById('imageContainer');
const resultImage = document.getElementById('resultImage');
const downloadBtn = document.getElementById('downloadBtn');
const errorMessage = document.getElementById('errorMessage');
const errorText = document.getElementById('errorText');

const styleButtons = document.querySelectorAll('.style-btn');
const suggestionChips = document.querySelectorAll('.suggestion-chip');

let selectedStyle = 'realistic';
let currentImageUrl = null;

async function checkOllamaStatus() {
    setStatus('loading', 'Checking...');
    try {
        const response = await fetch(`${API_BASE}/api/status`);
        const data = await response.json();
        
        const providerName = {
            'huggingface': 'HuggingFace',
            'ollama': 'Ollama',
            'local': 'Local SD'
        }[data.provider] || data.provider;
        
        if (data.status === 'connected' || data.status === 'configured' || data.status === 'ready') {
            setStatus('connected', `${providerName} Ready`);
            forgeBtn.disabled = false;
        } else if (data.status === 'no_token') {
            setStatus('disconnected', 'HF Token Required');
            forgeBtn.disabled = true;
        } else {
            setStatus('disconnected', `${providerName} Offline`);
            forgeBtn.disabled = true;
        }
    } catch (error) {
        setStatus('disconnected', 'Server Offline');
        forgeBtn.disabled = true;
    }
}

function setStatus(state, text) {
    statusIndicator.className = 'status-indicator ' + state;
    statusIndicator.querySelector('.status-text').textContent = text;
}

function showResult(type) {
    placeholder.classList.add('hidden');
    imageContainer.classList.add('hidden');
    errorMessage.classList.add('hidden');
    
    if (type === 'placeholder') {
        placeholder.classList.remove('hidden');
    } else if (type === 'image') {
        imageContainer.classList.remove('hidden');
    } else if (type === 'error') {
        errorMessage.classList.remove('hidden');
    }
}

async function generateAvatar() {
    const prompt = promptInput.value.trim();
    if (!prompt) return;
    
    showResult('placeholder');
    forgeBtn.classList.add('loading');
    forgeBtn.disabled = true;
    
    try {
        const response = await fetch(`${API_BASE}/api/generate`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                prompt: prompt,
                style: selectedStyle
            })
        });
        
        const data = await response.json();
        
        if (data.success && data.image_url) {
            currentImageUrl = data.image_url;
            resultImage.src = `${API_BASE}${data.image_url}?t=${Date.now()}`;
            showResult('image');
        } else {
            errorText.textContent = data.error || 'Generation failed. Please try again.';
            showResult('error');
        }
    } catch (error) {
        errorText.textContent = 'Failed to connect to server. Is it running?';
        showResult('error');
    } finally {
        forgeBtn.classList.remove('loading');
        forgeBtn.disabled = false;
    }
}

async function downloadImage() {
    if (!currentImageUrl) return;
    
    try {
        const response = await fetch(`${API_BASE}${currentImageUrl}`);
        const blob = await response.blob();
        const url = URL.createObjectURL(blob);
        
        const a = document.createElement('a');
        a.href = url;
        a.download = `dpforge_${Date.now()}.png`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    } catch (error) {
        console.error('Download failed:', error);
    }
}

promptInput.addEventListener('input', () => {
    charCount.textContent = promptInput.value.length;
});

promptInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !forgeBtn.disabled) {
        generateAvatar();
    }
});

forgeBtn.addEventListener('click', generateAvatar);
downloadBtn.addEventListener('click', downloadImage);

styleButtons.forEach(btn => {
    btn.addEventListener('click', () => {
        styleButtons.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        selectedStyle = btn.dataset.style;
    });
});

suggestionChips.forEach(chip => {
    chip.addEventListener('click', () => {
        promptInput.value = chip.dataset.prompt;
        charCount.textContent = promptInput.value.length;
        promptInput.focus();
    });
});

checkOllamaStatus();
setInterval(checkOllamaStatus, 30000);
