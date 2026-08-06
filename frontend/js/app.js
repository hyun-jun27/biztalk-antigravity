// API Endpoint Base Address (In production / Vercel, this can be relative or dynamic)
const API_BASE = window.location.origin;

// DOM Elements
const targetButtons = document.querySelectorAll(".target-btn");
const inputText = document.getElementById("inputText");
const btnConvert = document.getElementById("btnConvert");
const btnText = document.getElementById("btnText");
const loadingSpinner = document.getElementById("loadingSpinner");
const resultPanel = document.getElementById("resultPanel");
const outputText = document.getElementById("outputText");
const btnCopy = document.getElementById("btnCopy");
const toast = document.getElementById("toast");

let activeTarget = "boss";

// 1. Target Audience Selection Toggle
targetButtons.forEach(button => {
    button.addEventListener("click", () => {
        // Deactivate previous button
        targetButtons.forEach(btn => {
            btn.classList.remove("active");
            btn.setAttribute("aria-checked", "false");
        });

        // Activate clicked button
        button.classList.add("active");
        button.setAttribute("aria-checked", "true");
        activeTarget = button.dataset.target;
    });
});

// 2. Loading State Toggle Controller
function setLoading(isLoading) {
    if (isLoading) {
        btnConvert.disabled = true;
        loadingSpinner.style.display = "block";
        btnText.textContent = "변환 작업 진행 중...";
    } else {
        btnConvert.disabled = false;
        loadingSpinner.style.display = "none";
        btnText.textContent = "비즈니스 말투로 변환하기";
    }
}

// 3. API Request for Tone Conversion
async function convertTone() {
    const text = inputText.value.trim();

    if (!text) {
        showToast("변환할 원본 내용을 입력해 주세요.", true);
        inputText.focus();
        return;
    }

    setLoading(true);

    try {
        const response = await fetch(`${API_BASE}/api/convert`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                text: text,
                target_audience: activeTarget
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP Error: ${response.status}`);
        }

        const data = await response.json();
        
        // Show result panel and set output text
        resultPanel.style.display = "block";
        outputText.value = data.converted_text;
        
        // Smoothly scroll down to the result if on mobile
        resultPanel.scrollIntoView({ behavior: "smooth" });

    } catch (error) {
        console.error("Conversion failed:", error);
        showToast("변환 중 오류가 발생했습니다. 잠시 후 다시 시도해 주세요.", true);
    } finally {
        setLoading(false);
    }
}

// 4. Clipboard Copy Handler
async function copyToClipboard() {
    const resultText = outputText.value;
    if (!resultText) return;

    try {
        await navigator.clipboard.writeText(resultText);
        showToast("📋 비즈니스 메시지가 클립보드에 복사되었습니다.");
    } catch (err) {
        // Fallback for older browsers
        outputText.select();
        document.execCommand("copy");
        showToast("📋 텍스트가 복사되었습니다.");
    }
}

// 5. Toast Message Controller
let toastTimeout;
function showToast(message, isWarning = false) {
    clearTimeout(toastTimeout);
    
    toast.textContent = message;
    if (isWarning) {
        toast.style.borderColor = "#ef4444";
    } else {
        toast.style.borderColor = "var(--primary)";
    }
    
    toast.classList.add("show");

    toastTimeout = setTimeout(() => {
        toast.classList.remove("show");
    }, 3000);
}

// Event Listeners
btnConvert.addEventListener("click", convertTone);
btnCopy.addEventListener("click", copyToClipboard);
