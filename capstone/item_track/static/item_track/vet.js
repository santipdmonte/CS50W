//Listener to services-price input
// Get the input elements and select the treatment
document.addEventListener('DOMContentLoaded', function() {
    inputTreatment = document.getElementById('treatment');
    inputTreatment_id = document.getElementById('treatment_id');
    inputPrice = document.getElementById('price');
    
    // Add an event listener to the inputTreatment element
    inputTreatment.addEventListener('input', function() {
        const selectedTreatment = inputTreatment.value;
        const option = document.querySelector(`#datalistOptions option[value="${selectedTreatment}"]`);

        // Save as value the treatment_id
        inputTreatment_id.value = option.dataset.treatment_id;

        if (option && option.dataset.price) {
            inputPrice.value = option.dataset.price;
        } else {
            inputPrice.value = '';
        }
    });

    // document.querySelector('#add_btn').addEventListener('click', (event) => {
    //     // Save as value the treatment_id
    //     inputTreatment_id.value = option.dataset.treatment_id;
    // });
});

// JavaScript to add the form to the table
function addRow() {
    // Get the values entered in the form
    var amount = document.getElementById('amount').value;
    var treatment = document.getElementById('treatment').value;
    var observation = document.getElementById('observationInput').value;
    var price = document.getElementById('price').value;
    var treatment_id = document.getElementById('treatment_id').value;

    // Create a new row in the table
    // var table = document.getElementById('table');
    var table = document.querySelector('#table tbody');
    var row = table.insertRow();

    // Insert cells in the new row
    var amountCell = row.insertCell();
    var descriptionCell = row.insertCell();
    var observationCell = row.insertCell();
    var priceCell = row.insertCell();
    var actionsCell = row.insertCell();

    amountCell.innerHTML = amount;
    descriptionCell.innerHTML = treatment;
    if (!observation){
    observationCell.innerHTML = '-';
    }
    else{
    observationCell.innerHTML = observation;
    }
    priceCell.innerHTML = '$' + price;
    actionsCell.innerHTML = '<button class="btn btn-outline-danger btn-sm" onclick="deleteRow(this)">Delete</button> <button class="btn btn-outline-primary btn-sm" onclick="editRow(this)">Edit</button>'; // Delete and edit buttons

    // Update the data attributes with the values
    amountCell.setAttribute('data-amount', amount);
    descriptionCell.setAttribute('data-treatment', treatment);
    descriptionCell.setAttribute('data-treatment_id', treatment_id);
    observationCell.setAttribute('data-observation', observation);
    priceCell.setAttribute('data-price', price);

    // Clear the form fields
    document.getElementById('amount').value = 1;
    document.getElementById('treatment').value = '';
    document.getElementById('observationInput').value = '';
    document.getElementById('price').value = '';
}


function deleteRow(button) {
    var row = button.parentNode.parentNode;
    var table = document.getElementById('table');
    table.deleteRow(row.rowIndex);
}


function editRow(button) {
    var row = button.parentNode.parentNode;
    var amountCell = row.cells[0];
    var descriptionCell = row.cells[1];
    var observationCell = row.cells[2];
    var priceCell = row.cells[3];

    // Get the current values from the row
    var currentAmount = amountCell.getAttribute('data-amount');
    var currentTreatment = descriptionCell.getAttribute('data-treatment');
    var currentObservation = observationCell.getAttribute('data-observation');
    var currentPrice = priceCell.getAttribute('data-price');

    // Set the values in the modal input fields
    document.getElementById('editAmount').value = currentAmount;
    document.getElementById('editTreatment').value = currentTreatment;
    document.getElementById('editObservation').value = currentObservation;
    document.getElementById('editPrice').value = currentPrice;

    // Show the modal
    $('#editModal').modal('show');

    // Save the edited values on modal save
    document.getElementById('saveChangesEditBtn').onclick = function() {
        var editedAmount = document.getElementById('editAmount').value;
        var editedTreatment = document.getElementById('editTreatment').value;
        var editedObservation = document.getElementById('editObservation').value;
        var editedPrice = document.getElementById('editPrice').value;

        amountCell.innerHTML = editedAmount;
        descriptionCell.innerHTML = editedTreatment;
        if (observationCell){
            observationCell.innerHTML = editedObservation;
        }
        else{
            observationCell.innerHTML = '-';
        }
        priceCell.innerHTML = '$' + editedPrice;

        // Update the data attributes with the edited values
        amountCell.setAttribute('data-amount', editedAmount);
        descriptionCell.setAttribute('data-treatment', editedTreatment);
        observationCell.setAttribute('data-observation', editedObservation);
        priceCell.setAttribute('data-price', editedPrice);

        // Hide the modal
        $('#editModal').modal('hide');
    };
};


function send(event, csrf_token){
    // Save the table into a json
    var tableRows = document.querySelectorAll('#table tbody tr');

    var tableData = [];

    var clientData = {
        name: document.getElementById("ClientName").value,
        observation: document.getElementById("ClientObservation").value
        };
        tableData.push(clientData);

    for (var i = 0; i < tableRows.length; i++) {
        var row = tableRows[i];
        // Get the values from the row cells
        var amount = row.cells[0].getAttribute('data-amount');
        var treatment = row.cells[1].getAttribute('data-treatment');
        var treatment_id = row.cells[1].getAttribute('data-treatment_id');
        var observation = row.cells[2].getAttribute('data-observation');
        var price = row.cells[3].getAttribute('data-price');

        var rowData = {
            amount: amount,
            treatment_id: treatment_id,
            treatment: treatment,
            observation: observation,
            price: price
        };
        tableData.push(rowData);
    }

    // Send the data as JSON to the server
    fetch('/transaction', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrf_token
        },
        body: JSON.stringify(tableData)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log(data);
    })
    .catch(error => {
        console.error('Fetch error:', error);
    });
}