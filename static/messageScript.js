
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
    }
}

/**
 * Function to receive and display messages.
 * Sends a POST request to '/receive' endpoint with a message.
 * Receives a JSON response with a 'message' key.
 * Displays the received message in the chat-box.
 */
function receiveMessage() {
    // Set up the request options
    const requestOptions = {
        // Specify the HTTP method
        method: 'POST',
        // Set the 'Content-Type' header to 'application/json'
        headers: { 'Content-Type': 'application/json' },
        // Set the request body to an empty string
        body: JSON.stringify({recipient_id: document.getElementById('recipient_id').value})
    }
    // Send a POST request to '/receive' with a placeholder message
    fetch('/receive', requestOptions)
    // Parse the response
    .then(response => response.json())
    // Extract the 'message' from the JSON and display it in the chat-box
    .then(data => {
        let messages = ''
        for (const message of data) {
            messages += `<p>${message.sender_id}: ${message.content}</p>`
        }
        document.getElementById('chat-messages').innerHTML = messages
    })
}

function updateChat() {
    sendMessage();
    setTimeout(receiveMessage, 500);
}


// Periodically check for new messages (for demonstration purposes)
setInterval(receiveMessage, 5000); // Fetch new messages every 5 seconds
