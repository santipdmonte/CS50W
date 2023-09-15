//Listener to services-price input
// Get the input elements and select the item element
document.addEventListener('DOMContentLoaded', function() {
    inputItem = document.getElementById('addItem');
    inputItem_id = document.getElementById('item_id');
    inputPrice = document.getElementById('addPrice');
    inputBarcode = document.getElementById('addBarcode');
    
    // Add an event listener to the inputItem element
    inputItem.addEventListener('input', function() {
        const selectedItem = inputItem.value;
        const option = document.querySelector(`#datalistOptions option[value="${selectedItem}"]`);

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

        console.log(selectedBarcode);
        
        fetch(`/item/barcode/${selectedBarcode}`)
        .then(response => {
            if (!response.ok) {
                inputItem.value = '';
                inputItem_id.value = '';
                inputPrice.value = '';
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
              console.log(item);
            } 
          })
          .catch(error => {
            console.log('Hubo un error:', error);
          });
    });
});

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

    // Save the edited values on modal save
    document.querySelector('#saveChangesEditBtn').onclick = function() {
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
                <tr>
                    <td>${show_amount} ${element.item.name} ${show_observation}</td>
                    <td>$${(element.item.price * amount).toFixed(2)}</td>
                </tr>
                `;
            lastRow.insertAdjacentHTML('beforebegin', newElementHTML);

            // Update the total
            document.querySelector(`#total-${consult_id}`).innerHTML = transaction.total;
            
        })
        .catch(error => {
            // Handle any errors that may occur during the fetch or JSON parsing
            console.error('Error:', error);
        });


        // amountCell.innerHTML = editedAmount;
        // descriptionCell.innerHTML = editedItem;
        // if (observationCell){
        //     observationCell.innerHTML = editedObservation;
        // }
        // else{
        //     observationCell.innerHTML = '-';
        // }
        // priceCell.innerHTML = '$' + editedPrice;

        // // Update the data attributes with the edited values
        // amountCell.setAttribute('data-amount', editedAmount);
        // descriptionCell.setAttribute('data-item', editedItem);
        // observationCell.setAttribute('data-observation', editedObservation);
        // priceCell.setAttribute('data-price', editedPrice);

        // Hide the modal
        $('#addModal').modal('hide');
    };
};
