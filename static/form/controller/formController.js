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
        this.validationInstance = null; // Add this line
        // add event listeners
        this.mbtiElement.addEventListener('input', this.handleMbtiChange.bind(this));
        this.childhoodElement.addEventListener('input', this.handleChildhoodChange.bind(this));
        this.relationshipElement.addEventListener('input', this.handleRelationshipChange.bind(this));
        this.workingElement.addEventListener('input', this.handleWorkingChange.bind(this));
        this.formElement.addEventListener('submit', this.handleSubmit.bind(this));
        this.skip_button.addEventListener('click', this.handleSkip.bind(this));
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
        this.service.validateAndSubmit(this.model);
    }
    handleSkip(event) {
        event.preventDefault(); // prevent the default action

        document.getElementById("form").style.display = "none";
        document.getElementById("chat").style.display = "block";

    }
}
