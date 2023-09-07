function check_consult(csrf_token, consult_id){

    row = document.querySelector(`#row-${consult_id}`);

    row.style.display = 'none';

    // Send to the PUT request to the server
    fetch(`/front_desk`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrf_token
        },
        body: JSON.stringify({
            consult_id: consult_id,
        })
    })
    .then(response => response.json())
    .catch(error => console.log(error))

}