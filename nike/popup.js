// Restores select box and checkbox state using the preferences
// stored in chrome.storage.
function restore_options() {
    // Use default value color = 'red' and likesColor = true.
    chrome.storage.sync.get({
        selectedSize: '',
        selectedBankType: '',
        selectedProductCode: ''
    }, function(items) {
        //console.log(items.selectedSize);
        //console.log(items.selectedBankType);
        //console.log(items.selectedProductCode);

        document.getElementById('selectedSize').textContent = items.selectedSize;
        document.getElementById('selectedBankCode').textContent = items.selectedBankType;
        document.getElementById('selectedProductCode').textContent = items.selectedProductCode;

        var link = "http://www.nikestore.com.hk/product/" + items.selectedProductCode + "/detail.htm";
        document.getElementById("selectedProductCodeLink").href = link;
    });
}
document.addEventListener('DOMContentLoaded', restore_options);
