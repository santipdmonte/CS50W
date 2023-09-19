//Listener to services-price input
// Get the input elements and select the item element
document.addEventListener('DOMContentLoaded', function() {
    inputItem = document.getElementById('addItem');
    inputItem_id = document.getElementById('item_id');
    inputPrice = document.getElementById('addPrice');
    inputBarcode = document.getElementById('addBarcode');
    inputAmount = document.getElementById('addAmount');
    
    // Add an event listener to the inputItem element
    inputItem.addEventListener('input', function() {
        const selectedItem = inputItem.value;
        const option = document.querySelector(`#datalistOptions option[value="${selectedItem}"]`);

        // Reset Amount Value
        if (option){
            inputAmount.value = 1;
            validate_stock(selectedItem, option.dataset.stock, option.dataset.stock_min);
        }
    
        // Save as value the item_id
        inputItem_id.value = option.dataset.item_id;
        inputBarcode.value = option.dataset.barcode;

        if (option && option.dataset.price) {
            inputPrice.value = option.dataset.price;
        } else {
            inputPrice.value = '';
        }

        if (option && option.dataset.barcode) {
            inputBarcode.value = option.dataset.barcode;
        } else {
            inputBarcode.value = '';
        }
    });

    inputBarcode.addEventListener('input', function() {
        const selectedBarcode = inputBarcode.value;
        
        fetch(`/item/barcode/${selectedBarcode}`)
        .then(response => {
            if (!response.ok) {
                inputItem.value = '';
                inputItem_id.value = '';
                inputPrice.value = '';
                inputAmount.value = 1;
                throw new Error('No se encontró el artículo.');
            }
            return response.json();
          })
          .then(item => {
            // If fund the item
            if (item) {
              inputItem.value = item.name;
              inputItem_id.value = item.id;
              inputPrice.value = item.price;
              inputAmount.value = 1;
              validate_stock(item.name, item.stock, item.stock_min);
            } 
          })
          .catch(error => {
            console.log('Hubo un error:', error);
          });
    });
});


function validate_stock(item, stock, stock_min) {

    // No stock
    if (stock < 1) {
        alert(`${item} NO STOCK! \nStock: ${stock}`);
        $('#addModal').modal('hide');

    }
    // Low Stock
    else if (stock) {
        document.querySelector('#addAmount').max = stock;
        if (parseInt(stock) <= parseInt(stock_min)) {
            alert(`LOW STOCK! \nStock: ${stock}`);
        }
    }

}


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


function addRow(button, consult_id, csrf_token){
    // Clear the old values
    document.querySelector('#addAmount').value = 1;
    document.querySelector('#addItem').value = '';
    document.querySelector('#addObservation').value = '';
    document.querySelector('#addPrice').value = '';
    inputBarcode.value = '';

    // Show the modal
    $('#addModal').modal('show');

    // Focus the barcode
    $('#addModal').on('shown.bs.modal', function () {
        inputBarcode.focus();
    });
    confirmAddBtn
    // Save values
    document.querySelector('#confirmAddBtn').onclick = function() {
        var amount = document.querySelector('#addAmount').value;
        var item = document.querySelector('#addItem').value;
        var item_id = document.querySelector('#item_id').value;
        var observation = document.querySelector('#addObservation').value;
        var price = document.querySelector('#addPrice').value;

        // Send to the POST request to the server
        fetch(`/front_desk`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrf_token
            },
            body: JSON.stringify({
                consult_id: consult_id,
                amount: amount,
                item_id: item_id,
                observation: observation,
                price: price,
            })
        })
        //Update the table with the new row
        .then(response => response.json()) // Parse the JSON response
        .then(data => {
            console.log(data.transaction); 

            var transaction = data.transaction;

            // Add new element to the table
            element = transaction.movements[transaction.movements.length - 1];
            var consultRow = document.querySelector('#row-' + consult_id);
            var lastRow = consultRow.querySelector('tbody tr:last-child');

            var show_amount = "";
            if (amount > 1) {
                show_amount = `(x${amount})`;
            }
        
            var show_observation = "";
            if (observation) {
                show_observation = `[${observation}]`;
            }

            var newElementHTML = `
                <tr id="row-${element.item.id}" data-id="${element.item.id}" class="selectable-row" onclick="clickrow(event, ${element.item.id}, ${transaction.id})">
                    <td>${show_amount} ${element.item.name} ${show_observation}</td>
                    <td>$${(element.item.price * amount).toFixed(2)}</td>
                </tr>
                `;
            lastRow.insertAdjacentHTML('beforebegin', newElementHTML);

            // Update the total
            trans_total = parseFloat(transaction.total).toFixed(2);
            document.querySelector(`#total-${consult_id}`).innerHTML = `$${(trans_total)}`;
            
        })
        .catch(error => {
            // Handle any errors that may occur during the fetch or JSON parsing
            console.error('Error:', error);
        });

        // Hide the modal
        $('#addModal').modal('hide');
    };
};


var selected_consult_id = null;

function clickrow(event, id, consult_id){
    var clickedRow = event.currentTarget;
    var columnInRow = clickedRow.querySelector('td');
    
    // Get all the selected rows
    var selectedRows = document.querySelectorAll('.selected-row');

    // If click in a new consult delte the selected-row class
    if (selected_consult_id != null && selected_consult_id != consult_id) {

        document.querySelector(`#delete-${selected_consult_id}`).style.display = 'none';
        
        selectedRows.forEach(function(row) {
            var columnInCurrentRow = row.querySelector('td');
            columnInCurrentRow.style.backgroundColor = '';
            row.classList.remove('selected-row');
        });
    }

    // Select the row. If the row is selected, unselect it
    if (columnInRow.style.backgroundColor === 'red') {
        columnInRow.style.backgroundColor = '';
        clickedRow.classList.remove('selected-row');
    } else {
        columnInRow.style.backgroundColor = 'red';
        clickedRow.classList.add('selected-row');
    }
    var selectedRows = document.querySelectorAll('.selected-row');
    
    // Update the consult_id of the selected row
    selected_consult_id = consult_id;

    // Show/hide the delete button
    if (selectedRows.length > 0 ){
        document.querySelector(`#delete-${consult_id}`).style.display = 'block';
    } else {
        document.querySelector(`#delete-${consult_id}`).style.display = 'none';
    }
}

function deleteRow(event, consult_id, csrf_token){

    var selectedRows = document.querySelectorAll('.selected-row');

    selectedRows.forEach( row => {
        var movementId = row.getAttribute('data-id');

        // Config DELETE fetch request
        fetch(`movement/${movementId}`, {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': csrf_token, 
                'Content-Type': 'application/json',
            },
        })
        .then(response => response.json()) // Parse the JSON response
        .then(data => {
            var transaction = data.transaction;

            // Diplay none the row
            row.style.display = 'none';

            // Update the total
            trans_total = parseFloat(transaction.total).toFixed(2);
            document.querySelector(`#total-${consult_id}`).innerHTML = `$${(trans_total)}`;
        })
        .catch(function(error) {
            // Maneja errores de red u otros errores
            console.error('Error de red o procesamiento:', error);
        });
    })

    // Hide the delete button
    document.querySelector(`#delete-${consult_id}`).style.display = 'none';

    // TODO If th transaction has no movements, delete the consult

}
