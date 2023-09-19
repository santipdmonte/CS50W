//Listener to services-price input
// Get the input elements and select the item element
document.addEventListener('DOMContentLoaded', function() {
    inputItem = document.getElementById('addItem');
    inputItem_id = document.getElementById('item_id');
    inputPrice = document.getElementById('addPrice');
    inputBarcode = document.getElementById('addBarcode');
    inputAddAmount = document.getElementById('addAmount');
    currentStock = document.getElementById('currentStock');
    
    // Add an event listener to the inputItem element
    inputItem.addEventListener('input', function() {
        const selectedItem = inputItem.value;
        const option = document.querySelector(`#datalistOptions option[value="${selectedItem}"]`);


        
        // When found the item, focus on the amount input
        if (option){
            inputAddAmount.focus();
            // Save as value the item_id
            inputItem_id.value = option.dataset.item_id;
            inputBarcode.value = option.dataset.barcode;
        }

        // Manage Stock input
        if (option && option.dataset.stock) {
            currentStock.value = option.dataset.stock;
        } else {
            currentStock.value = '';
        }

        // Manage Price input
        if (option && option.dataset.price) {
            inputPrice.value = option.dataset.price;
        } else {
            inputPrice.value = '';
        }

        // Manage Barcode input
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
                currentStock.value = '';
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
              currentStock.value = item.stock;
              inputAddAmount.focus();
              console.log(item);
            } 
          })
          .catch(error => {
            console.log('Hubo un error:', error);
          });
    });
});

function saveChanges(csrf_token){

    itemId = inputItem_id.value;
    itemName = inputItem.value;
    itemPrice = inputPrice.value;
    itemBarcode = inputBarcode.value;
    itemAmount = document.getElementById('addAmount').value;

    fetch(`/item/update/${itemId}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrf_token
        },
        body: JSON.stringify({
            itemName: itemName,
            itemPrice: itemPrice,
            itemBarcode: itemBarcode,
            itemAmount: itemAmount
        })
    })
    .then(response => response.json())
    .then(() => {
        // Add alert
        const successAlert = document.createElement('div');
        successAlert.classList.add('alert', 'alert-success', 'mt-2');
        successAlert.textContent = `${itemName} successfully updated!`;

        // Add alert to the form
        const form = document.querySelector('form');
        form.appendChild(successAlert);

        cancelChanges()});
}

function cancelChanges(){
    
    inputItem.value = '';
    inputItem_id.value = '';
    inputPrice.value = '';
    inputBarcode.value = '';
    currentStock.value = '';
    document.getElementById('addAmount').value = 0;

    console.log(inputBarcode);
    inputBarcode.focus();
}
