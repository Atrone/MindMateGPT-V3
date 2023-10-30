class ContactFormServices {

    validateAndSubmit(formModel) {
        $('#contact_form').data('bootstrapValidator').validate();
        const isValid = $('#contact_form').data('bootstrapValidator').isValid();
        if (isValid) {
            this.submitForm(formModel);
        } else {
            console.error('Error during form validation and submission:', error);
        }
    }

    submitForm(model) {
        const url = 'https://mindmategpt.com/api/getForm';
        const formData = new FormData();

        formData.append('mbti', model.mbti);
        formData.append('childhood', model.childhood);
        formData.append('relationship', model.relationship);
        formData.append('working', model.working);

        // add Session header value if necessary
        const headers = {'Session': document.getElementById("session").textContent,
        'taskResult': null ? "" : localStorage.getItem('taskResult')};

        fetch(url, {
            method: 'POST',
            body: formData,
            headers: headers
        })
        .then(response => {
            // handle the response from the backend API endpoint
            document.getElementById("form").style.display = "none";
            document.getElementById("chat").style.display = "block";
            document.getElementById('input2').focus(); // Refocus on the input
        })
        .catch(error => {
            // handle any errors that occur during the form submission process
            console.error(error);
        });
    }
    initializeFormValidation() {
        $('#contact_form').bootstrapValidator({
            feedbackIcons: {
                valid: 'glyphicon glyphicon-ok',
                invalid: 'glyphicon glyphicon-remove',
                validating: 'glyphicon glyphicon-refresh'
            },
            fields: {
                childhood: {
                    validators: {
                  stringLength: {min:0}
                }
                },
                relationship: {
                    validators: {
                  stringLength: {min:0}
                }

                },
                mbti: { validators: { notEmpty: { message: 'Please supply your MBTI' } } },
                working: {
                    validators: {
                  stringLength: {min:0}
                }
                }

            }
        }).on('success.form.bv', function(e) {
            // Prevent form submission
            e.preventDefault();
        });
    }

}
