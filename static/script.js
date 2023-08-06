let input = document.getElementById('input2');
let chat = document.getElementById('chat2');
let messages = document.getElementById('messages');
let startButton = document.getElementById('startButton');

startButton.addEventListener('click', function() {
    startButton.style.display = 'none';
    window.scrollTo(0,document.body.scrollHeight);
    input.focus();
});

input2.addEventListener('keydown', function(event) {
  var sesh = document.getElementById("session");
    if (event.key === 'Enter') {
        event.preventDefault();
        if (input.value.trim() !== '') {
            let message = document.createElement('p');
            let messageDiv = document.createElement('div');
            messageDiv.className = 'message';
            message.textContent = input.value;
            messageDiv.appendChild(message);
            messages.appendChild(messageDiv);
            input.value = '';
            messages.scrollTop = messages.scrollHeight;
            input.style.display = 'none';

            let loadingDiv = document.createElement('div');
            let loading = document.createElement('p');
            loadingDiv.className = 'message response';
            loading.textContent = '.';
            loadingDiv.appendChild(loading);
            messages.appendChild(loadingDiv);
            messages.scrollTop = messages.scrollHeight;

            let count = 0;
            let loadingInterval = setInterval(function() {
                count++;
                loading.textContent = '.'.repeat(count % 4);
                messages.scrollTop = messages.scrollHeight;
            }, 500);


            fetch('https://mindmategpt.herokuapp.com/api/therapistGPT', {
                method: 'POST',
                headers: {
                  "Content-Type": "application/json",
                  'Session': sesh.textContent // Include the session ID in the headers
                },
                body: JSON.stringify({body:{message:message.textContent}}),
                key_body: JSON.stringify({key_body:{key: "BOILER"}})
            })
            .then(response => response.text())
            .then(data => {
                clearInterval(loadingInterval);
                messages.removeChild(loadingDiv);
                let responseDiv = document.createElement('div');
                responseDiv.className = 'message response';
                let response = document.createElement('p');
                response.textContent = data;
                response.textContent = data.replace(/\"/g, "").replace(/\n/g, " "); // Remove quotes and new lines
                responseDiv.appendChild(response);
                messages.appendChild(responseDiv);
                messages.scrollTop = messages.scrollHeight;
                input.style.display = 'block';
                input.focus(); // Refocus on the input
            })
            .catch((error) => {
                console.error('Error:', error);
            });
    }
}});
