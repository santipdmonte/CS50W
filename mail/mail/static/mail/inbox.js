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

        // Check if the email was read
        backgroundColor = "white"
        if (email.read){
          backgroundColor = "#e8e8e8";
        };

        // Check the length of the body
        email_body = email.body
        console.log(email.body.length)
        if (email_body.length > 25){
          email_body = email_body.slice(0, 25) + '...';
        }

        const emailRow = document.createElement('div');
        emailRow.className = 'container';
        emailContent = `
        <div class="row" style="border-bottom: 1px D3D3D3 solid; background-color: ${backgroundColor}; cursor: pointer">
            <div class="col">
                ${email.sender}
            </div>
            <div class="col" >
                <p>${email.subject} - <span style="color:grey">${email_body}</span></p>
            </div>
            <div class="text-left">
                <div class="col">
                    ${email.timestamp}
                </div>
            </div>
        </div>`;

        emailRow.innerHTML = `<b>${emailContent}</b>`
        if (email.read){
          emailRow.innerHTML = emailContent
        };

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
    
    const archive_btn = document.createElement('button');
    archive_btn.className = 'btn btn-primary';
    archive_btn.innerHTML = `
    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-archive-fill" viewBox="0 0 16 16">
      <path d="M12.643 15C13.979 15 15 13.845 15 12.5V5H1v7.5C1 13.845 2.021 15 3.357 15h9.286zM5.5 7h5a.5.5 0 0 1 0 1h-5a.5.5 0 0 1 0-1zM.8 1a.8.8 0 0 0-.8.8V3a.8.8 0 0 0 .8.8h14.4A.8.8 0 0 0 16 3V1.8a.8.8 0 0 0-.8-.8H.8z"/>
    </svg>
     Archive`
    if (email.archived){ 
      archive_btn.className = 'btn btn-secondary';
      archive_btn.innerHTML = `
      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-archive-fill" viewBox="0 0 16 16">
        <path d="M12.643 15C13.979 15 15 13.845 15 12.5V5H1v7.5C1 13.845 2.021 15 3.357 15h9.286zM5.5 7h5a.5.5 0 0 1 0 1h-5a.5.5 0 0 1 0-1zM.8 1a.8.8 0 0 0-.8.8V3a.8.8 0 0 0 .8.8h14.4A.8.8 0 0 0 16 3V1.8a.8.8 0 0 0-.8-.8H.8z"/>
      </svg>
       Unarchive`
    }

    const reply_btn = document.createElement('button');
    reply_btn.className = 'btn btn-primary mr-3';
    reply_btn.innerHTML = `
    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-reply-all-fill" viewBox="0 0 16 16">
      <path d="M8.021 11.9 3.453 8.62a.719.719 0 0 1 0-1.238L8.021 4.1a.716.716 0 0 1 1.079.619V6c1.5 0 6 0 7 8-2.5-4.5-7-4-7-4v1.281c0 .56-.606.898-1.079.62z"/>
      <path d="M5.232 4.293a.5.5 0 0 1-.106.7L1.114 7.945a.5.5 0 0 1-.042.028.147.147 0 0 0 0 .252.503.503 0 0 1 .042.028l4.012 2.954a.5.5 0 1 1-.593.805L.539 9.073a1.147 1.147 0 0 1 0-1.946l3.994-2.94a.5.5 0 0 1 .699.106z"/>
    </svg>
     Reply ` 
    
    view = document.querySelector('#email-view')
    view.innerHTML = 
    `
    <div style="height: 50vh;">
      <h3>${email.subject}</h3>
      <div class="d-flex justify-content-between mr-3">
        <p>${email.sender}<p><p>${email.timestamp}</p>
      </div>
      <hr>
      <p>${email.body}</p>
    </div>
    `
    view.append(reply_btn)
    view.append(archive_btn)


    // Change Archive and Unarchive
    archive_btn.addEventListener('click', () => ch_archive(email));
    reply_btn.addEventListener('click', () => reply_email(email));
    
  });
  
}

function ch_archive(email){
  console.log("ch_archive")
  if (email.archived){
    fetch(`/emails/${email.id}`, {
      method: 'PUT',
      body: JSON.stringify({
          archived: false
      })
    })
    
  } else {
    fetch(`/emails/${email.id}`, {
      method: 'PUT',
      body: JSON.stringify({
          archived: true
      })
    })
  }
  load_mailbox('inbox')
}


function reply_email(email){
  console.log("reply_email")
  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = email.sender;
  if (email.subject.startsWith("Re: ")){
    document.querySelector('#compose-subject').value = email.subject;
  } else {
    document.querySelector('#compose-subject').value = 'Re: ' + email.subject;
  }
  document.querySelector('#compose-body').value = `${email.timestamp} ${email.sender} wrote: ${email.body}`;

  // Work with the compose form
  document.querySelector("#compose-form").addEventListener('submit', () => send_mail());
}