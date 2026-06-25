
console.log("Agentic AI Frontend Loaded");

document.addEventListener("DOMContentLoaded", () => {

    // ======================================================
    // ELEMENTS
    // ======================================================

    const chatBox = document.getElementById("chat-box");
    const input = document.getElementById("message-input");

    const sendBtn = document.getElementById("send-btn");
    const clearBtn = document.getElementById("clear-btn");
    const saveBtn = document.getElementById("save-btn");
    const newChatBtn = document.getElementById("new-chat-btn");

    const historyContainer =
        document.getElementById("history-container");

    const CHAT_HISTORY_KEY =
        "agentic_ai_chat";

    let heroMarkup =
        document.querySelector(".hero")?.outerHTML || "";

    // ======================================================
    // INITIALIZATION
    // ======================================================

    loadHistory();

    bindUI();

    refreshHistoryPanel();


    // ======================================================
    // EVENT BINDINGS
    // ======================================================

    function bindUI() {

        sendBtn?.addEventListener(
            "click",
            sendMessage
        );

        clearBtn?.addEventListener(
            "click",
            clearChat
        );

        newChatBtn?.addEventListener(
            "click",
            startNewConversation
        );

        saveBtn?.addEventListener(
            "click",
            saveChatAsText
        );

        // ENTER KEY SUPPORT

        input?.addEventListener(
            "keydown",

            function (event) {

                if (
                    event.key === "Enter" &&
                    !event.shiftKey
                ) {

                    event.preventDefault();

                    sendMessage();
                }
            }
        );

        bindSuggestionButtons();
    }


    // ======================================================
    // SUGGESTION BUTTONS
    // ======================================================

    function bindSuggestionButtons() {

        document
            .querySelectorAll(".suggestion-card")

            .forEach((card) => {

                card.addEventListener(

                    "click",

                    () => {

                        sendMessage(
                            card.innerText.trim()
                        );
                    }
                );
            });
    }


    // ======================================================
    // SEND MESSAGE
    // ======================================================

    async function sendMessage(
        predefinedQuestion = null
    ) {

        const question = (
            predefinedQuestion ||
            input.value
        ).trim();

        if (!question)
            return;

        document
            .querySelector(".hero")
            ?.remove();

        addMessage(question, "user");

        input.value = "";

        const loader =
            addTyping();

        try {

            const response =
                await fetch("/chat", {

                    method: "POST",

                    headers: {

                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({

                        question: question,

                        thread_id:
                            "sridhar_001"
                    })
                });

            const data =
                await response.json();

            console.log(data);

            loader.remove();

            addBotMessage(

                data.answer ||
                data.response ||
                "No response received.",

                data.latency_seconds ||
                "-"
            );

        }

        catch (error) {

            console.error(error);

            loader.remove();

            addBotMessage(
                "Backend connection failed.",
                "-"
            );
        }
    }


    // ======================================================
    // USER MESSAGE
    // ======================================================

    function addMessage(
        text,
        type
    ) {

        const div =
            document.createElement("div");

        div.className =
            `message ${type}`;

        div.innerHTML = `

            <div class="bubble">

                ${escapeHtml(text)}

            </div>
        `;

        chatBox.appendChild(div);

        scrollBottom();

        saveHistory();
    }


    // ======================================================
    // BOT MESSAGE
    // ======================================================

    function addBotMessage(
        answer,
        latency = "-"
    ) {

        const div =
            document.createElement("div");

        div.className =
            "message bot";

        div.innerHTML = `

            <div class="bubble bubble-bot">

                ${escapeHtml(answer)}

                <div class="meta">

                    ⚡ Latency:
                    ${latency}s

                </div>

            </div>
        `;

        chatBox.appendChild(div);

        scrollBottom();

        saveHistory();
    }


    // ======================================================
    // LOADER
    // ======================================================

    function addTyping() {

        const div =
            document.createElement("div");

        div.className =
            "message bot";

        div.innerHTML = `

            <div class="bubble bubble-bot">

                <div class="typing">

                    <span></span>
                    <span></span>
                    <span></span>

                </div>

            </div>
        `;

        chatBox.appendChild(div);

        scrollBottom();

        return div;
    }


    // ======================================================
    // CLEAR CHAT
    // ======================================================

    function clearChat() {

        localStorage.removeItem(
            CHAT_HISTORY_KEY
        );

        chatBox.innerHTML =
            heroMarkup;

        bindSuggestionButtons();

        refreshHistoryPanel();
    }


    // ======================================================
    // NEW CHAT
    // ======================================================

    function startNewConversation() {

        clearChat();
    }


    // ======================================================
    // SAVE CHAT
    // ======================================================

    function saveChatAsText() {

        const text =
            chatBox.innerText;

        const blob =
            new Blob(
                [text],
                {
                    type:
                        "text/plain"
                }
            );

        const url =
            URL.createObjectURL(blob);

        const a =
            document.createElement("a");

        a.href = url;

        a.download =
            "agentic_ai_chat.txt";

        a.click();

        URL.revokeObjectURL(url);
    }


    // ======================================================
    // HISTORY
    // ======================================================

    function saveHistory() {

        localStorage.setItem(

            CHAT_HISTORY_KEY,

            chatBox.innerHTML
        );

        refreshHistoryPanel();
    }


    function loadHistory() {

        const history =
            localStorage.getItem(
                CHAT_HISTORY_KEY
            );

        if (history) {

            chatBox.innerHTML =
                history;
        }
    }


    function refreshHistoryPanel() {

        if (!historyContainer)
            return;

        const history =
            localStorage.getItem(
                CHAT_HISTORY_KEY
            );

        if (!history) {

            historyContainer.innerHTML = `

                <div class="history-empty">

                    No saved conversations yet

                </div>
            `;

            return;
        }

        historyContainer.innerHTML = `

            <div class="history-item">

                Latest Conversation

            </div>
        `;
    }


    // ======================================================
    // HELPERS
    // ======================================================

    function scrollBottom() {

        chatBox.scrollTop =
            chatBox.scrollHeight;
    }


    function escapeHtml(text) {

        return text

            .replace(/&/g, "&amp;")

            .replace(/</g, "&lt;")

            .replace(/>/g, "&gt;")

            .replace(/"/g, "&quot;")

            .replace(/'/g, "&#039;");
    }

});

