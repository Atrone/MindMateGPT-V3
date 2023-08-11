class ChatService {
    constructor() {
        this.session = document.getElementById("session").textContent;
    }

    async sendMessage(message) {
        const response = await fetch('https://mindmategpt.com/api/therapistGPT', {
            method: 'POST',
            headers: {
              "Content-Type": "application/json",
              'Session': this.session
            },
            body: JSON.stringify({message: message})
        });
        const data = await response.text();
        return data.replace(/\"/g, "").replace(/(\r\n|\n|\r)/gm, " ");
    }

    async downloadJournal(email) {
        const data = {recipient: email};
        const response = await fetch("https://mindmategpt.com/api/download", {
            method: "POST",
            mode: "cors",
            cache: "no-cache",
            credentials: "same-origin",
            headers: {
              "Content-Type": "application/json",
              'Session': this.session
            },
            redirect: "follow",
            referrerPolicy: "no-referrer",
            body: JSON.stringify(data),
        });
        const task = await response.json();
        return task.task_id;
    }
    async checkTaskStatus(taskId) {
        const response = await fetch(`https://mindmategpt.com/api/task_status/${taskId}`);
        const data = await response.json();
        return data;
    }

    startPolling(taskId) {
        return new Promise(async (resolve, reject) => {
            const intervalId = setInterval(async () => {
                try {
                    const status = await this.checkTaskStatus(taskId);
                    if (status.status === "completed") {
                        clearInterval(intervalId);  // Stop polling
                        document.cookie = `taskResult=${encodeURIComponent(status.result.gpt4)}; path=/; max-age=86400 * 7`;  // The result is stored for 1 day (86400 seconds)
                        resolve(status.result.gpt4);
                    } else if (status.status === "error") {  // Add any other statuses that indicate an error
                        clearInterval(intervalId);  // Stop polling
                        reject(new Error("Task encountered an error"));
                    }
                } catch (error) {
                    clearInterval(intervalId);
                    reject(error);
                }
            }, 5000);  // Poll every 5 seconds, adjust as necessary
        });
    }

    async handleTask(email) {
        const taskId = await this.downloadJournal(email);
        try {
            const result = await this.startPolling(taskId);
            return result;
        } catch (error) {
            throw error;  // Handle error or throw it to be caught outside of this function
        }
    }
}