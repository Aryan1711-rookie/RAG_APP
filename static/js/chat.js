async function askQuestion() {

    const input = document.getElementById("question");
    const question = input.value.trim();

    if (!question) return;

    addMessage(question, "user");
    input.value = "";

    const botBubble = addMessage("", "bot");

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

        const data = await response.json();

        botBubble.innerHTML = data.answer;

    } catch (error) {

        botBubble.innerHTML =
            "Error contacting server";

        console.error(error);
    }
}
function addMessage(text, sender) {
    const chatBox = document.getElementById("chat-box");
    const msg = document.createElement("div");

    msg.classList.add("message", sender);
    msg.innerHTML = `<div class="bubble">${text}</div>`;

    chatBox.appendChild(msg);
    chatBox.scrollTop = chatBox.scrollHeight;

    return msg.querySelector(".bubble");
}