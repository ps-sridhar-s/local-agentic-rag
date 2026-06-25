const chatBox = document.getElementById("chat-box");
const input = document.getElementById("message-input");

loadHistory();

async function sendMessage() {

    let question = input.value.trim();

    if (!question) return;

    if(document.querySelector(".welcome"))
        document.querySelector(".welcome").remove();

    addMessage(question,"user");

    input.value="";

    const typingDiv = addTyping();

    try{

        const response = await fetch(
            "http://127.0.0.1:8111/chat",
            {
                method:"POST",

                headers:{
                    "Content-Type":"application/json"
                },

                body:JSON.stringify({
                    question:question,
                    thread_id:"sridhar_001"
                })
            }
        );

        const data = await response.json();

        typingDiv.remove();

        addBotMessage(
            data.answer,
            data.latency_seconds,
            data.evaluation_score
        );

    }

    catch(error){

        typingDiv.remove();

        addBotMessage(
            "Backend connection failed."
        );
    }
}

function addMessage(text,type){

    const div=document.createElement("div");

    div.className=`message ${type}`;

    div.innerHTML=`
        <div class="bubble">
            ${text}
        </div>
    `;

    chatBox.appendChild(div);

    scrollBottom();

    saveHistory();
}

function addBotMessage(answer,latency="",score=""){

    const div=document.createElement("div");

    div.className="message bot";

    div.innerHTML=`
        <div class="bubble">
            ${answer}

            <div class="meta">
                Latency : ${latency}s |
                Score : ${score}
            </div>
        </div>
    `;

    chatBox.appendChild(div);

    scrollBottom();

    saveHistory();
}

function addTyping(){

    const div=document.createElement("div");

    div.className="message bot";

    div.innerHTML=`
        <div class="bubble">
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

function scrollBottom(){
    chatBox.scrollTop=chatBox.scrollHeight;
}

input.addEventListener("keydown",e=>{

    if(e.key==="Enter" && !e.shiftKey){

        e.preventDefault();

        sendMessage();
    }
});

function saveHistory(){

    localStorage.setItem(
        "chatHistory",
        chatBox.innerHTML
    );
}

function loadHistory(){

    let history=localStorage.getItem(
        "chatHistory"
    );

    if(history){

        chatBox.innerHTML=history;
    }
}

function clearChat(){

    localStorage.removeItem(
        "chatHistory"
    );

    location.reload();
}