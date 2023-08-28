document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // Email click
  // document.querySelector('.email-row').addEventListener('click', () => open_email());

  // By default, load the inbox
  load_mailbox('inbox');
});

// Send the compose mail
function send_mail(){

    // Save form information
    const recipients = document.querySelector('#compose-recipients').value;
    const subject = document.querySelector('#compose-subject').value;
    const body = document.querySelector('#compose-body').value;

    console.log(recipients, subject, body)

    fetch('/emails', {
        method: 'POST',
        body: JSON.stringify({
            recipients: recipients,
            subject: subject,
            body: body
        })
      })
      .then(response => response.json())
      .then(result => {
          // Print result
          console.log(result);
      });

      // Load user sent inbox
      // TODO <Complete>
}

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

  // Work with the compose form
  document.querySelector("#compose-form").addEventListener('submit', () => send_mail());

}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  
  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
  
  // Load emails
  const view = document.querySelector('#emails-view');

  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    if (emails && emails.length > 0) {

      // Print emails
      console.log(emails);
      emails.forEach(email => {
        console.log(email.read)
        backgroundColor = "white"
        if (email.read){
          backgroundColor = "#D3D3D3";
        };
        view.innerHTML += `
        <div class="container">
          <div class="row email-row" data-id=${email.id} style="border: 1px grey solid; background-color: ${backgroundColor}; cursor: pointer";>
            <div class="col">
              <b>${email.sender}</b>
            </div>
            <div class="col" >
              <p>${email.subject} - <span style="color:grey">${email.body}</span></p>
            </div>
            <div class="text-left">
              <div class="col" style="color:grey">
                ${email.timestamp}
              </div>
            </div>
          </div>
        </div>`;
      })

    } else {
      view.innerHTML += `<p>Mailbox Empty.<p>`;
    }

  });
}

// function open_email(){
//   // Show compose view and hide other views
//   document.querySelector('#emails-view').style.display = 'none';
//   document.querySelector('#compose-view').style.display = 'none';
//   document.querySelector('#email-view').style.display = 'block'; 

//   console.log("open_email")

//   fetch(`/emails/${div.data.id}`)
//   .then(response => response.json())
//   .then(email => {
//     // Print email
//     console.log(email);

//   });

// }
