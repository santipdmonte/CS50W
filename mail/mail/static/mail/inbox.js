document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  
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
      console.log("emails: ",emails);
      emails.forEach(email => {
        backgroundColor = "white"
        if (email.read){
          backgroundColor = "#D3D3D3";
        };
        const emailRow = document.createElement('div');
        emailRow.className = 'container';
        emailRow.innerHTML = `
        <div class="row emailrow" style="border: 1px grey solid; background-color: ${backgroundColor}; cursor: pointer">
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
        </div>`;

        // Agregar el emailRow al view
        view.appendChild(emailRow);

        // Agregar un event listener a emailRow
        emailRow.addEventListener('click', function() {
            // Manejar el clic en emailRow aquí
            open_email(email.id);
        });
      })

    } else {
      view.innerHTML += `<p>Mailbox Empty.<p>`;
    }

  });

}

function open_email(id){
  console.log("open_email")

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'block'; 

  fetch(`/emails/${id}`)
  .then(response => response.json())
  .then(email => {

    // Mark the email as read
    fetch(`/emails/${id}`, {
      method: 'PUT',
      body: JSON.stringify({
          read: true
      })
    })

    // Print email
    console.log(email);

    view = document.querySelector('#email-view')
    view.innerHTML = 
    `
    <div>
      <h4>${email.subjet}</h4>
      <p>${email.sender} - ${email.timestamp}</p>
      <p>${email.body}</p>
    </div>
    `

  });

}
