$('#downloadButton').on('click', async (e) => {
                          var sesh = document.getElementById("session");
                          var keyInput = document.getElementById('key');
                          var downloadInput = document.getElementById('downloadInput');
                          console.log(keyInput.value)
                          // show bot message
                          var data = {message:"", key: keyInput.value, recipient: downloadInput.value};


                          // Default options are marked with *
                          const response = await fetch("https://mindmategpt.herokuapp.com/api/download", {
                            method: "POST", // *GET, POST, PUT, DELETE, etc.
                            mode: "cors", // no-cors, *cors, same-origin
                            cache: "no-cache", // *default, no-cache, reload, force-cache, only-if-cached
                            credentials: "same-origin", // include, *same-origin, omit
                            headers: {
                              "Content-Type": "application/json",
                              'Session': sesh.textContent // Include the session ID in the headers
                            },
                            redirect: "follow", // manual, *follow, error
                            referrerPolicy: "no-referrer", // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
                            body: JSON.stringify(data), // body data type must match "Content-Type" header
                          });
                          return response.json(); // parses JSON response into native JavaScript objects
});


$('#contact_form').bootstrapValidator({
        // To use feedback icons, ensure that you use Bootstrap v3.1.0 or later
        feedbackIcons: {
            valid: 'glyphicon glyphicon-ok',
            invalid: 'glyphicon glyphicon-remove',
            validating: 'glyphicon glyphicon-refresh'
        },
        fields: {
             childhood: {
                validators: {
                     stringLength: {
                        min: 0,
                    }
                }
            },
            relationship: {
                validators: {
                  stringLength: {min:0, max:200}
                }
            },
            mbti: {
                validators: {
                    notEmpty: {
                        message: 'Please supply your MBTI'
                    }
                }
            },
            working: {
                validators: {
                      stringLength: {
                        min: 0,
                        max: 200,
                        message:'Please enter at least 0 characters and no more than 200'
                    }
                    }
                }


            }
        }).on('success.form.bv', function(event) {

  event.preventDefault(); // prevent the default form submission behavior
  const form = event.target;
  const formData = new FormData(form);
  const url = 'https://mindmategpt.herokuapp.com/api/getForm';
  var myDiv = document.getElementById("intro");
  var myDiv2 = document.getElementById("chat");
  var sesh = document.getElementById("session");
  var title = document.getElementById("welcome_title");
  var input = document.getElementById('input2');

  // use AJAX to submit the form data to the backend API endpoint
  fetch(url, {
    method: 'POST',
    body: formData,
    headers: {'Session': sesh.textContent}
  })
  .then(response => {
    // handle the response from the backend API endpoint
    myDiv.style.display = "none";
    myDiv2.style.display = "block";
    input.focus(); // Refocus on the input
  })
  .catch(error => {
    // handle any errors that occur during the form submission process
    console.error(error);
  });
});



