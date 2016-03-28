// Saves options to chrome.storage.sync.
function save_options() {
    var size = document.getElementById('size').value;
    var bankType = document.getElementById('bankType').value;
    var productCode = document.getElementById('productCode').value;

    console.log(size);
    console.log(bankType);
    console.log(productCode);
    chrome.storage.sync.set({
        selectedSize: size,
        selectedBankType: bankType,
        selectedProductCode: productCode
    }, function() {
        // Update status to let user know options were saved.
        var status = document.getElementById('status');
        status.textContent = 'Options saved.';
        setTimeout(function() {
            status.textContent = '';
        }, 750);
    });
}

// Restores select box and checkbox state using the preferences
// stored in chrome.storage.
function restore_options() {
    // Use default value color = 'red' and likesColor = true.
    chrome.storage.sync.get({
        selectedSize: '11',
        selectedBankType: 'Master',
        selectedProductCode: 'code'
    }, function(items) {
        document.getElementById('size').value = items.selectedSize;
        document.getElementById('bankType').value = items.selectedBankType;
        document.getElementById('productCode').value = items.selectedProductCode;
    });
}
document.addEventListener('DOMContentLoaded', restore_options);
document.getElementById('save').addEventListener('click',
    save_options);
