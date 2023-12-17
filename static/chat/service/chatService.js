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
                        localStorage.setItem('taskResult', encodeURIComponent(status.result.gpt4));  // The result is stored persistently until explicitly removed
                        resolve(status.result.gpt4);
                    } else if (status.status === "error") {  // Add any other statuses that indicate an error
                        clearInterval(intervalId);  // Stop polling
                        localStorage.setItem('taskResult', encodeURIComponent(status.result.gpt4));  // The result is stored persistently until explicitly removed
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
    async checkPaymentStatus() {
        const response = await fetch(`https://mindmategpt.com/api/payment_status`);
        const data = await response.json();
        return data;
    }

    startPollingPayment() {
        return new Promise(async (resolve, reject) => {
            const intervalId = setInterval(async () => {
                try {
                    const status = await this.checkPaymentStatus();
                    if (status.status === "completed") {
                        clearInterval(intervalId);
                        resolve("Payment Completed Successfully.");
                    } else if (status.status === "error") {
                        clearInterval(intervalId);
                        reject(new Error("Payment encountered an error."));
                    }
                } catch (error) {
                    clearInterval(intervalId);
                    reject(error);
                }
            }, 3000); // Poll every 1 seconds
        });
    }

    async handlePayment() {
        try {
            const result = await this.startPollingPayment();
            console.log(result);
            document.getElementById('buyButton').style.display = 'none';
            document.getElementById('buyButton2').style.display = 'none';
            document.getElementById('downloadInput').style.display = 'block';
            document.getElementById('downloadButton').style.display = 'block';
        } catch (error) {
            console.error(error); // Handle the error appropriately
        }
    }
}
