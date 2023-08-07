// contact-form/model/contactFormModel.js

class ContactFormModel {
    constructor() {
        this.mbti = '';
        this.childhood = '';
        this.relationship = '';
        this.working = '';
        this.summary = '';
        this.insight = '';
    }

    init() {}

    updateMbti(mbti) {
        this.mbti = mbti;
    }

    updateChildhood(childhood) {
        this.childhood = childhood;
    }

    updateRelationship(relationship) {
        this.relationship = relationship;
    }

    updateWorking(working) {
        this.working = working;
    }

    updateInsight(insight) {
        this.insight = insight;
    }

    updateSummary(summary) {
        this.summary = summary;
    }
}
