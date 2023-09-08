//Listener to services-price input
// Get the input elements and select the item element
document.addEventListener('DOMContentLoaded', function() {
    inputItem = document.getElementById('addItem');
    inputItem_id = document.getElementById('item_id');
    inputPrice = document.getElementById('addPrice');
    
    // Add an event listener to the inputItem element
    inputItem.addEventListener('input', function() {
        const selectedItem = inputItem.value;
        const option = document.querySelector(`#datalistOptions option[value="${selectedItem}"]`);

        // Save as value the item_id
        inputItem_id.value = option.dataset.item_id;

        if (option && option.dataset.price) {
            inputPrice.value = option.dataset.price;
        } else {
            inputPrice.value = '';
        }
    });

    // document.querySelector('#add_btn').addEventListener('click', (event) => {
    //     // Save as value the item_id
    //     inputItem_id.value = option.dataset.item_id;
    // });
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
    console.log('addRow');

    // Clear the old values
    document.querySelector('#addAmount').value = 1;
    document.querySelector('#addItem').value = '';
    document.querySelector('#addObservation').value = '';
    document.querySelector('#addPrice').value = '';

    // Show the modal
    $('#addModal').modal('show');

    // Save the edited values on modal save
    document.querySelector('#saveChangesEditBtn').onclick = function() {
        var amount = document.querySelector('#addAmount').value;
        var item = document.querySelector('#addItem').value;
        var item_id = document.querySelector('#item_id').value;
        var observation = document.querySelector('#addObservation').value;
        var price = document.querySelector('#addPrice').value;

        console.log(consult_id, amount, item, observation, price);

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
