document.querySelector('button').addEventListener('click', sendMessage);

function sendMessage() {
    const input = document.getElementById('user-input');
    const message = input.value.trim();
    if (!message) return;

    addMessage(message, 'user');
    input.value = '';

    fetch('/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message })
    })
    .then(res => res.json())
    .then(data => {
        addMessage(data.response, 'das');
    })
    .catch(err => {
        addMessage("Oops, something went wrong!", 'das');
        console.error(err);
    });
}

function addMessage(text, sender) {
    const log = document.getElementById('chat-log');
    const msg = document.createElement('div');
    msg.className = `chat-message ${sender}-message`;
    msg.textContent = text;
    log.appendChild(msg);
    log.scrollTop = log.scrollHeight;
}
