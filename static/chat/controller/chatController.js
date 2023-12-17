class ChatController {
    constructor(model, service) {
        this.model = model;
        this.service = service;
        this.inputElement = document.getElementById('input2');
        this.downloadButton = document.getElementById('downloadButton');
        this.buyButton = document.getElementById('buyButton');
        this.buyButton2 = document.getElementById('buyButton2');
        this.downloadInputElement = document.getElementById('downloadInput');
        this.finishedButton = document.getElementById('finished');
        this.modal = document.getElementById('myModal');
        this.modalClose = document.getElementsByClassName('close')[0];
        this.messagesElement = document.getElementById('messages');
        this.inputElement.addEventListener('keydown', this.handleMessageInput.bind(this));
        this.downloadButton.addEventListener('click', this.handleDownloadClick.bind(this));
        this.buyButton.addEventListener('click', this.handleBuyClick.bind(this));
        this.buyButton2.addEventListener('click', this.handleBuyClick.bind(this));
        this.finishedButton.addEventListener('click', this.handleFinishedClick.bind(this));
        this.modalClose.addEventListener('click', this.handleCloseClick.bind(this));
        window.addEventListener('click', this.handleWindowClick.bind(this));
    }

    handleMessageInput(event) {
        if (event.key === 'Enter') {
            event.preventDefault();
            if (this.inputElement.value.trim() !== '') {
                this.model.updateMessage(this.inputElement.value);
                this.displayUserMessage(this.inputElement.value);
                this.handleMessageSubmission();
                this.inputElement.value = '';
            }
        }
    }

    displayUserMessage(message) {
        let messageDiv = document.createElement('div');
        messageDiv.className = 'message';
        let messageElement = document.createElement('p');
        messageElement.textContent = message;
        messageDiv.appendChild(messageElement);
        this.messagesElement.appendChild(messageDiv);
    }

    async handleMessageSubmission() {
        // display loading animation
        let loadingDiv = document.createElement('div');
        let loading = document.createElement('p');
        loadingDiv.className = 'message response';
        loading.textContent = '.';
        loadingDiv.appendChild(loading);
        this.messagesElement.appendChild(loadingDiv);
        let count = 0;
        let loadingInterval = setInterval(function() {
                count++;
                loading.textContent = '.'.repeat(count % 4);
                messages.scrollTop = messages.scrollHeight;
        }, 500);
        const response = await this.service.sendMessage(this.model.message);
        clearInterval(loadingInterval);

        // clear loading animation
        this.messagesElement.removeChild(loadingDiv);

        // display received message
        let responseDiv = document.createElement('div');
        responseDiv.className = 'message response';
        let responseElement = document.createElement('p');
        responseElement.textContent = response;
        responseElement.style.textAlign = "right";
        responseDiv.appendChild(responseElement);
        this.messagesElement.appendChild(responseDiv);
        this.messagesElement.scrollTop = this.messagesElement.scrollHeight;
        this.inputElement.style.display = 'block';
        this.inputElement.focus();
        
        let paragraphs = document.querySelectorAll('p');
    
        // Loop through 
        paragraphs.forEach(function(p) {
        p.innerHTML = p.innerHTML.replace(/\\n/g, '<br>');
        });
        
    }

    handleBuyClick(event){
        this.service.handlePayment()
        .then(result => {
            // If you want to handle the successful result here
            console.log(result);
        })
        .catch(error => {
            // If you want to handle errors here
            console.error(error);
        });

    }

    async handleDownloadClick(event) {
        event.preventDefault();
        const email = this.downloadInputElement.value;
        document.getElementById('loadingSpinner2').style.display = 'block';
        const data = await this.service.handleTask(email);
        document.getElementById('loadingSpinner2').style.display = 'none';
    }

    handleFinishedClick(event) {
        this.modal.style.display = 'block';
    }

    handleCloseClick(event) {
        this.modal.style.display = 'none';
    }

    handleWindowClick(event) {
        if (event.target == this.modal) {
            this.modal.style.display = 'none';
        }
    }
}
