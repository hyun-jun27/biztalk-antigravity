// API base URL configuration
// 로컬 파일 실행(file:///) 시 로컬서버 호출, 동일 호스트 서빙 시 호스트 도메인 자동 타겟팅
const API_BASE = window.location.origin.startsWith('file:') 
    ? "http://localhost:8080" 
    : window.location.origin;

document.addEventListener("DOMContentLoaded", () => {
    const inputText = document.getElementById("inputText");
    const charCounter = document.getElementById("charCounter");
    const targetButtons = document.querySelectorAll(".target-btn");
    const convertBtn = document.getElementById("convertBtn");
    const outputText = document.getElementById("outputText");
    const copyBtn = document.getElementById("copyBtn");
    const loadingOverlay = document.getElementById("loadingOverlay");
    const toast = document.getElementById("toast");
    const toastMsg = document.getElementById("toastMsg");

    let selectedTarget = null;

    // 1. Character Counter
    inputText.addEventListener("input", () => {
        const length = inputText.value.length;
        charCounter.textContent = `${length}자`;
    });

    // 2. Target Audience Selection (Single selection)
    targetButtons.forEach(btn => {
        btn.addEventListener("click", () => {
            targetButtons.forEach(b => b.classList.remove("active"));
            
            if (selectedTarget === btn.dataset.target) {
                // Deselect if already active
                selectedTarget = null;
            } else {
                btn.classList.add("active");
                selectedTarget = btn.dataset.target;
            }
        });
    });

    // 3. Tone Conversion handler
    convertBtn.addEventListener("click", async () => {
        const text = inputText.value.trim();

        if (!text) {
            showToast("변환할 원본 내용을 입력해 주세요.", "warning");
            inputText.focus();
            return;
        }

        if (!selectedTarget) {
            showToast("수신 대상을 선택해 주세요.", "warning");
            return;
        }

        // Set Loading state UI
        setLoading(true);

        try {
            const response = await fetch(`${API_BASE}/api/convert`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    text: text,
                    target_audience: selectedTarget
                })
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || "서버 응답 오류가 발생했습니다.");
            }

            const data = await response.json();
            outputText.value = data.converted_text;
            copyBtn.disabled = false;
            showToast("성공적으로 변환되었습니다!", "success");

        } catch (error) {
            console.error("API Call Error:", error);
            showToast(error.message || "변환 중 문제가 발생했습니다. 다시 시도해 주세요.", "error");
        } finally {
            setLoading(false);
        }
    });

    // 4. Clipboard Copy Handler
    copyBtn.addEventListener("click", async () => {
        const textToCopy = outputText.value;
        if (!textToCopy) return;

        try {
            await navigator.clipboard.writeText(textToCopy);
            showToast("클립보드에 메시지가 복사되었습니다!", "success");
        } catch (err) {
            // Fallback for browsers that don't support navigator.clipboard
            outputText.select();
            document.execCommand("copy");
            showToast("메시지가 선택 및 복사되었습니다!", "success");
        }
    });

    // Loading State Helper
    function setLoading(isLoading) {
        if (isLoading) {
            convertBtn.classList.add("loading");
            convertBtn.disabled = true;
            loadingOverlay.classList.add("active");
        } else {
            convertBtn.classList.remove("loading");
            convertBtn.disabled = false;
            loadingOverlay.classList.remove("active");
        }
    }

    // Toast Alert Helper
    function showToast(message, type = "success") {
        toastMsg.textContent = message;
        
        // Dynamic Icon mapping
        const icon = toast.querySelector("i");
        icon.className = ""; // Reset
        if (type === "success") {
            icon.className = "fa-solid fa-circle-check";
            toast.style.borderColor = "var(--accent-purple)";
        } else if (type === "warning") {
            icon.className = "fa-solid fa-triangle-exclamation";
            toast.style.borderColor = "#f59e0b";
        } else {
            icon.className = "fa-solid fa-circle-xmark";
            toast.style.borderColor = "#ef4444";
        }

        toast.classList.add("active");

        setTimeout(() => {
            toast.classList.remove("active");
        }, 3000);
    }
});
