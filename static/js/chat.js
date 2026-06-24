// async function askQuestion() {

//     const input = document.getElementById("question");
//     const question = input.value.trim();

//     if (!question) return;

//     addMessage(question, "user");
//     saveHistory(question);
//     input.value = "";

//     const botBubble = addMessage("", "bot");

//     try {

//         const response = await fetch("/ask", {
//             method: "POST",
//             headers: {
//                 "Content-Type": "application/json"
//             },
//             body: JSON.stringify({
//                 question: question
//             })
//         });

//         const data = await response.json();

//         botBubble.innerHTML = data.answer;

//     } catch (error) {

//         botBubble.innerHTML =
//             "Error contacting server";

//         console.error(error);
//     }
// }
// function addMessage(text, sender) {
//     const chatBox = document.getElementById("chat-box");
//     const msg = document.createElement("div");

//     msg.classList.add("message", sender);
//     msg.innerHTML = `<div class="bubble">${text}</div>`;

//     chatBox.appendChild(msg);
//     chatBox.scrollTop = chatBox.scrollHeight;

//     return msg.querySelector(".bubble");
// }
// function saveHistory(question){

//     let history =
//         JSON.parse(
//             localStorage.getItem("chat_history")
//         ) || [];

//     history.unshift(question);

//     history = history.slice(0,10);

//     localStorage.setItem(
//         "chat_history",
//         JSON.stringify(history)
//     );

//     renderHistory();
// }

// function renderHistory(){

//     const container =
//         document.getElementById("history-list");

//     if(!container) return;

//     const history =
//         JSON.parse(
//             localStorage.getItem("chat_history")
//         ) || [];

//     container.innerHTML = "";

//     history.forEach(item => {

//         const div =
//             document.createElement("div");

//         div.className = "history-item";

//         div.innerText = item;

//         container.appendChild(div);
//     });
// }

// document.addEventListener(
//     "DOMContentLoaded",
//     renderHistory
// );

async function askQuestion() {

    const input = document.getElementById("question");
    const chatBox = document.getElementById("chat-box");

    const question = input.value.trim();

    if (!question) return;

    const welcome = document.querySelector(".welcome");
    if (welcome) welcome.remove();

    addMessage(question, "user");

    input.value = "";

    const botMessage = addMessage("", "bot");

    botMessage.innerHTML = `
        <div class="typing">
            <span></span>
            <span></span>
            <span></span>
        </div>
    `;

    try {

        const response = await fetch("/ask", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                question: question
            })
        });

        const result = await response.json();

        let answer = result.answer || "No response";

        botMessage.innerHTML = "";

        let currentText = "";

        for (let i = 0; i < answer.length; i++) {

            currentText += answer[i];

            botMessage.innerHTML =
                marked.parse(currentText);

            chatBox.scrollTop =
                chatBox.scrollHeight;

            await new Promise(
                resolve => setTimeout(resolve, 5)
            );
        }

        if (result.sources &&
            result.sources.length > 0) {

            let sourcesHTML =
                `<div class="sources">
                    <h4>Sources</h4>`;

            const grouped = {};

            result.sources.forEach(src => {

                if (!grouped[src.source]) {
                    grouped[src.source] = [];
                }

                grouped[src.source].push(src.page);
            });

            for (const file in grouped) {

                sourcesHTML += `
        <div class="source-chip">
            📄 ${file}
            <br>
            <small>
                Pages: ${grouped[file].join(", ")}
            </small>
        </div>
    `;
            }
            sourcesHTML += `</div>`;

            botMessage.innerHTML += sourcesHTML;
        }

        const copyBtn =
            document.createElement("button");

        copyBtn.className =
            "copy-btn";

        copyBtn.innerText =
            "Copy";

        copyBtn.onclick = () => {

            navigator.clipboard.writeText(
                answer
            );

            copyBtn.innerText =
                "Copied";

            setTimeout(() => {
                copyBtn.innerText =
                    "Copy";
            }, 1500);
        };

        botMessage.appendChild(
            copyBtn
        );

    } catch (error) {

        botMessage.innerHTML = `
            <div class="error">
                Failed to get response.
            </div>
        `;

        console.error(error);
    }
}

function addMessage(text, sender) {

    const chatBox =
        document.getElementById("chat-box");

    const wrapper =
        document.createElement("div");

    wrapper.classList.add(
        "message",
        sender
    );

    wrapper.innerHTML = `
        <div class="avatar">
            ${sender === "user" ? "👤" : "👾"}
        </div>

        <div class="bubble">
            ${text}
        </div>
    `;

    chatBox.appendChild(wrapper);

    chatBox.scrollTop =
        chatBox.scrollHeight;

    return wrapper.querySelector(
        ".bubble"
    );
}