// Restores select box and checkbox state using the preferences
// stored in chrome.storage.
var infoLog = true
var debugLog = true

function log(type,logStr){
    
    if (type == "info" && infoLog)
    {
        console.log(logStr);
    }
    else if (type == "debug" && debugLog)
    {
        console.log(logStr);
    }
}

function restore_options() {
    // Use default value color = 'red' and likesColor = true.
    chrome.storage.sync.get({
        selectedSize: '',
        selectedBankType: '',
        selectedProductCode: ''
    }, function(items) {
        log("debug","items.selectedSize" + items.selectedSize);
        log("debug","items.selectedBankCode" + items.selectedBankCode);
        log("debug","items.selectedProductCode" + items.selectedProductCode);

        document.getElementById('selectedSize').textContent = items.selectedSize;
        document.getElementById('selectedBankCode').textContent = items.selectedBankType;
        document.getElementById('selectedProductCode').textContent = items.selectedProductCode;

        var link = "http://www.nikestore.com.hk/product/" + items.selectedProductCode + "/detail.htm";
        document.getElementById("selectedProductCodeLink").href = link;
    });
}
document.addEventListener('DOMContentLoaded', restore_options);
