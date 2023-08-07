class ChatModel {
    constructor() {
        this.session = document.getElementById("session").textContent;
        this.message = "";
    }

    updateMessage(newMessage) {
        this.message = newMessage;
    }
}