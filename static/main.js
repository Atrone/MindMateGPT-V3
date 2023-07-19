/**
 * Returns the current datetime for the message creation.
 */
function getCurrentTimestamp() {
	return new Date();
}


/**
 * Renders a message on the chat screen based on the given arguments.
 * This is called from the `showUserMessage` and `showBotMessage`.
 */
function renderMessageToScreen(args) {
	// local variables
	let displayDate = (args.time || getCurrentTimestamp()).toLocaleString('en-IN', {
		month: 'short',
		day: 'numeric',
		hour: 'numeric',
		minute: 'numeric',
	});
	let messagesContainer = $('.messages');

	// init element
	let message = $(`
	<li class="message ${args.message_side}">
		<div class="avatar"></div>
		<div class="text_wrapper">
			<div class="text">${args.text}</div>
			<div class="timestamp">${displayDate}</div>
		</div>
	</li>
	`);

	// add to parent
	messagesContainer.append(message);

	// animations
	setTimeout(function () {
		message.addClass('appeared');
	}, 0);
	messagesContainer.animate({ scrollTop: messagesContainer.prop('scrollHeight') }, 300);
}

/**
 * Displays the user message on the chat screen. This is the right side message.
 */
function showUserMessage(message, datetime) {
	renderMessageToScreen({
		text: message,
		time: datetime,
		message_side: 'right',
	});
}

/**
 * Displays the chatbot message on the chat screen. This is the left side message.
 */
function showBotMessage(message, datetime) {
	renderMessageToScreen({
		text: message,
		time: datetime,
		message_side: 'left',
	});
}

/**
 * Get input from user and show it on screen on button click.
 */
$('#send_button').on('click', async (e) => {
	var post_param = ($('#msg_input').val())

	// get and show message and reset input
	showUserMessage($('#msg_input').val());
	$('#msg_input').val('');
    var keyInput = document.getElementById('key');
    console.log(keyInput.value)

	// show bot message
	var ai = await postData({body:{message:post_param}}, {key: keyInput.value});
	showBotMessage(ai);


});

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
            first_name: {
                validators: {
                        stringLength: {
                        min: 2,
                    },
                        notEmpty: {
                        message: 'Please supply your first name'
                    }
                }
            },
             childhood: {
                validators: {
                     stringLength: {
                        min: 2,
                    },
                    notEmpty: {
                        message: 'Please supply your childhood'
                    }
                }
            },
            relationship: {
                validators: {
                    notEmpty: {
                        message: 'Please supply your relationship'
                    }
                }
            },
            mbti: {
                validators: {
                    notEmpty: {
                        message: 'Please supply your MBTI'
                    }
                }
            },
            growup: {
                validators: {
                    notEmpty: {
                        message: 'Please supply your upbringing area'
                    }
                }
            },
            live: {
                validators: {
                    notEmpty: {
                        message: 'Please supply your area of living'
                    }
                }
            },
            criminal: {
                validators: {
                     stringLength: {
                        min: 4,
                    },
                    notEmpty: {
                        message: 'Please supply your criminal'
                    }
                }
            },
            drugs: {
                validators: {
                     stringLength: {
                        min: 4,
                    },
                    notEmpty: {
                        message: 'Please supply your drugs'
                    }
                }
            },
            family: {
                validators: {
                    notEmpty: {
                        message: 'Please select your family'
                    }
                }
            },
            religion: {
                validators: {
                    notEmpty: {
                        message: 'Please supply your religion'
                    }
                }
            },
            education: {
                validators: {
                      stringLength: {
                        min: 3,
                        max: 200,
                        message:'Please enter at least 10 characters and no more than 200'
                    },
                    notEmpty: {
                        message: 'Please supply a education'
                    }
                    }
                },
            medication: {
                validators: {
                      stringLength: {
                        min: 1,
                        max: 200,
                        message:'Please enter at least 1 characters and no more than 200'
                    },
                    notEmpty: {
                        message: 'Please supply a medication'
                    }
                    }
                },
            working: {
                validators: {
                      stringLength: {
                        min: 1,
                        max: 200,
                        message:'Please enter at least 1 characters and no more than 200'
                    },
                    notEmpty: {
                        message: 'Please supply a working'
                    }
                    }
                }


            }
        }).on('success.form.bv', function(event) {

  event.preventDefault(); // prevent the default form submission behavior
  const form = event.target;
  const formData = new FormData(form);
  var name = formData.get('first_name');
  const url = 'https://mindmategpt.herokuapp.com/api/getForm';
  var myDiv = document.getElementById("intro");
  var myDiv2 = document.getElementById("chat");
  var sesh = document.getElementById("session");
  var title = document.getElementById("welcome_title");


  // use AJAX to submit the form data to the backend API endpoint
  fetch(url, {
    method: 'POST',
    body: formData,
    headers: {'Session': sesh.textContent}
  })
  .then(response => {
    // handle the response from the backend API endpoint
    title.textContent = 'MindMateGPT - ' + name;
    myDiv.style.display = "none";
    myDiv2.style.display = "block";
  })
  .catch(error => {
    // handle any errors that occur during the form submission process
    console.error(error);
  });
});

// Example POST method implementation:
async function postData(data, key_data) {
  var sesh = document.getElementById("session");

  // Default options are marked with *
  const response = await fetch("https://mindmategpt.herokuapp.com/api/therapistGPT", {
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
    key_body: JSON.stringify(key_data) // body data type must match "Content-Type" header
  });
  return response.json(); // parses JSON response into native JavaScript objects
}

/**
 * Set initial bot message to the screen for the user.
 */
$(window).on('load', function () {
  	var myDiv = document.getElementById("chat");
    myDiv.style.display = "none";
	showBotMessage('Hello there! Type in a message.');
});


