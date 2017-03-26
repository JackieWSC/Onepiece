//var productionCode="136027-130"; //air jordan 5
//var productionCode = "310810-107"; //air jordan 13 low
//var productionCode="705417-029"; //air jordan 7 - 1
//var productionCode="442961-029"; //air jordan 7 - 2

function Redirect(productionCode) {
    //window.location = "http://www.nikestore.com.hk/product/" + productionCode + "/detail.htm";

    var newCode = productionCode;
    //console.log(newCode);
    window.location = "http://www.nikestore.com.hk/product/" + newCode + "/detail.htm";

    // loop
    setTimeout(Redirect(newCode), 1000);
}

function getSizeFromOption(callback) {
    chrome.storage.sync.get({
        selectedSize: '',
        selectedProductCode: ''
    }, function(items) {
        //console.log(items.selectedSize);
        //console.log(items.selectedProductCode);
        callback(items.selectedSize, items.selectedProductCode);
    });
}

// main call here
getSizeFromOption(function(selectedSize, selectedProductCode) {
    //console.log(selectedProductCode);
    //Redirect(selectedProductCode);
    //setTimeout("Redirect()", 1000, selectedProductCode);
    if (selectedProductCode!="")
    {
        console.log(selectedProductCode);
        Redirect(selectedProductCode)
    }
    else
    {
        console.log("No ProductCode");
    }
})

//console.log(productCode);
//Redirect(productCode)
//setTimeout(
//    Redirect(productCode),
//    1000);
//setTimeout("Test()",250);

