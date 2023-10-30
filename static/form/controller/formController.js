// contact-form/controller/contactFormController.js

class ContactFormController {
    constructor(model, service) {
        this.model = model;
        this.service = service;
        this.formElement = document.getElementById('contact_form');
        this.mbtiElement = document.getElementById('mbti');
        this.childhoodElement = document.getElementById('childhood');
        this.relationshipElement = document.getElementById('relationship');
        this.workingElement = document.getElementById('working');
        this.skip_button = document.getElementById("skip_button");
        this.submit_button = document.getElementById("submitButtonForm");
        this.validationInstance = null; // Add this line
        // add event listeners
        const mbtiCookieValue = this.getCookie("mbti");
        const myDiv = document.getElementById("mbtiForm");

        // Check if the "mbti" cookie exists
        if (mbtiCookieValue) {
            // If the cookie exists, hide the div
            myDiv.style.display = "none";
        }

        this.mbtiElement.addEventListener('input', this.handleMbtiChange.bind(this));
        this.childhoodElement.addEventListener('input', this.handleChildhoodChange.bind(this));
        this.relationshipElement.addEventListener('input', this.handleRelationshipChange.bind(this));
        this.workingElement.addEventListener('input', this.handleWorkingChange.bind(this));
        this.formElement.addEventListener('submit', this.handleSubmit.bind(this));
        this.formElement.addEventListener('click', this.handleSubmitClick.bind(this));
        document.getElementById("submitButtonForm").addEventListener("click", function() {
            setTimeout(function() {
                document.getElementById("submitButtonForm").removeAttribute("disabled");
            }, 100); // you can adjust the timeout as necessary
        });

    }
    init() {
        this.service.initializeFormValidation();
    }

    handleMbtiChange(event) {
        this.model.updateMbti(event.target.value);
    }

    handleChildhoodChange(event) {
        this.model.updateChildhood(event.target.value);
    }

    handleRelationshipChange(event) {
        this.model.updateRelationship(event.target.value);
    }

    handleWorkingChange(event) {
        this.model.updateWorking(event.target.value);
    }

    handleSubmit(event) {
        event.preventDefault();
        if (!this.getCookie("mbti")) {
            document.cookie = `mbti=${encodeURIComponent(this.model.mbti)}; path=/; max-age=864000`;  // The result is stored for 1 day (86400 seconds)
        }

        this.service.validateAndSubmit(this.model);
    }

    handleSubmitClick(event) {
            setTimeout(function() {
                document.getElementById("submitButtonForm").removeAttribute("disabled");
            }, 100); // you can adjust the timeout as necessary
    }

    handleSkip(event) {
        event.preventDefault(); // prevent the default action

        document.getElementById("form").style.display = "none";
        document.getElementById("chat").style.display = "block";
        document.getElementById("input2").focus();
    }
    getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
    }

}
