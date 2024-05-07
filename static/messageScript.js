
/**
 * Function to send a message.
 * It retrieves the message from the chat input, sends a POST request to
 * the '/send' endpoint with the message, and then clears the chat input.
 */
function sendMessage() {
    // Get the chat input element
    const chatInput = document.getElementById('new_message');

    // Get the message from the chat input and trim any leading/trailing whitespace
    const message = chatInput.value.trim();
    
    // Only send the message if it is not empty
    if (message) {
        // Set up the request options
        const requestOptions = {
            // Specify the HTTP method
            method: 'POST',
            // Set the 'Content-Type' header to 'application/json'
            headers: { 'Content-Type': 'application/json' },
            // Convert the message to a JSON string and set it as the request body
            body: JSON.stringify({ message : message, recipient_id: document.getElementById('recipient_id').value })
        };
        
        // Send the POST request to '/send' endpoint
        fetch('/send', requestOptions);

        // Clear the chat input
        chatInput.value = '';

        // Make message object
        const messageObject = {
            username: 'you',
            content: message,
            timestamp: new Date().toISOString()
        };

        // Add the message to the chat box
        document.getElementById('chat-messages').innerHTML = wrapMessage(messageObject) + document.getElementById('chat-messages').innerHTML;
    }
}

/**
 * Function to receive and display messages.
 * Sends a POST request to '/receive' endpoint with a message.
 * Receives a JSON response with a 'message' key.
 * Displays the received message in the chat-box.
 */
function receiveMessage(old = false) {
    // Set up the request options
    const requestOptions = {
        // Specify the HTTP method
        method: 'POST',
        // Set the 'Content-Type' header to 'application/json'
        headers: { 'Content-Type': 'application/json' },
        // Set the request body to the recipient_id and old variables
        body: JSON.stringify({recipient_id: document.getElementById('recipient_id').value, old: old})
    }
    // Send a POST request to '/receive' with a placeholder message
    fetch('/receive', requestOptions)
    // Parse the response
    .then(response => response.json())
    // Extract the 'message' from the JSON and display it in the chat-box
    .then(data => {
        let messages = ''
        for (const message of data) {
            messages += wrapMessage(message)
        }
        
        // Add the messages to the top of the chat box
        document.getElementById('chat-messages').innerHTML = messages + document.getElementById('chat-messages').innerHTML;
    })
}


/**
 * Function to wrap message in a container with username and timestamp
 * @param {Object} message - The message object with 'username' and 'content' keys
 * @param {string} message.username - The username of the sender
 * @param {string} message.content - The content of the message
 * @param {string} message.timestamp - The timestamp of the message
 * @returns {string} The message wrapped in a container with username and timestamp
 */
function wrapMessage(message) {
    const timestamp = new Date(message.timestamp).toLocaleString(); // Get the current timestamp
    if (message.username == document.getElementById('username').value) {
        return `<div class="d-flex"><div class="card mb-2 me-5" style="background-color: #ced4da; width: fit-content"><span class="text-muted small mx-1">${message.username} (${timestamp})</span><div>${message.content}</div></div></div>`;
    }
    else {
        return `<div class="d-flex justify-content-end"><div class="card mb-2 ms-5" style="background-color: #e9ecef; width: fit-content"><span class="text-muted small mx-1">you (${timestamp})</span><div>${message.content}</div></div></div>`;
    }
}


/**
 * Function to send message on Enter key press.
 */
document.getElementById('new_message').addEventListener('keypress', function(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
});


function updateChat() {
    sendMessage();
    setTimeout(receiveMessage, 500);
}


// Initially load messages
receiveMessage(true);

// Periodically check for new messages
setInterval(receiveMessage, 5000);
