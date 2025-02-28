// Dynamic Starry Background
const canvas = document.getElementById('background');
const ctx = canvas.getContext('2d');

canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

let stars = [];

function createStars() {
    for (let i = 0; i < 100; i++) {
        stars.push({
            x: Math.random() * canvas.width,
            y: Math.random() * canvas.height,
            radius: Math.random() * 2,
            speed: Math.random() * 0.5
        });
    }
}

function animateStars() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    ctx.fillStyle = 'rgba(255, 255, 255, 0.8)';
    stars.forEach(star => {
        ctx.beginPath();
        ctx.arc(star.x, star.y, star.radius, 0, Math.PI * 2);
        ctx.fill();
        star.y += star.speed;
        if (star.y > canvas.height) {
            star.y = 0;
            star.x = Math.random() * canvas.width;
        }
    });
    
    requestAnimationFrame(animateStars);
}

createStars();
animateStars();

// Function to send the message and display in chatbox
function sendMessage() {
    var userInput = document.getElementById("user-input").value.trim();
    if (userInput === "") return;

    var chatBox = document.getElementById("chat-box");

    // Display user's message on the right side
    chatBox.innerHTML += `
        <div class="user-message">
            <p><strong>You:</strong> ${userInput}</p>
        </div>
    `;

    // Send message to the server (backend)
    fetch("/ask", {
        method: "POST",
        body: JSON.stringify({ "question": userInput }),
        headers: { "Content-Type": "application/json" }
    })
    .then(response => response.json())
    .then(data => {
        let botResponse = data.error ? data.error : Object.values(data).join(" ");
        
        // Display bot's response on the left side
        chatBox.innerHTML += `
            <div class="bot-message">
                <p><strong>Bot:</strong> ${botResponse}</p>
            </div>
        `;
        
        // Scroll chatbox to the bottom to show new messages
        chatBox.scrollTop = chatBox.scrollHeight;

        // Clear input field
        document.getElementById("user-input").value = "";
    })
    .catch(error => {
        console.error("Error:", error);
        chatBox.innerHTML += `
            <div class="bot-message">
                <p><strong>Bot:</strong> Error occurred. Try again.</p>
            </div>
        `;
        chatBox.scrollTop = chatBox.scrollHeight;
    });
}

// Handle "Enter" keypress to send message
document.getElementById("user-input").addEventListener("keypress", function (event) {
    if (event.key === "Enter") {
        sendMessage();
    }
});
