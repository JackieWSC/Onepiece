var defaultSize = "11";
var defaultSize1 = "7C";
var defaultSize2 = "8C";
var defaultSize3 = "9C";
var infoLog = true
var debugLog = false

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

function addToCart() {
    // click add to cart
    document.getElementsByClassName("btn-org block fLeft")[0].click();
}

function selectQty() {
    // click count
    document.getElementsByClassName("count select-btn")[0].click();
    var temp = document.getElementsByClassName("select-box-qty")[0];
    temp.children[0].click(); //amount = 1
}

function selectSize(size) {
    // click size
    document.getElementsByClassName("size select-btn")[0].click();

    // select size
    var temp = document.getElementsByClassName("select-box-size")[0];
    //temp.children[1].click();
    if (temp != undefined) {
        for (var i = 0; i < temp.childElementCount; i++) {
            tempSize = temp.children[i].innerText.trim();
            log("debug",tempSize);
            if (tempSize == size || tempSize == defaultSize1 || tempSize == defaultSize2 || tempSize == defaultSize3 ) {
                temp.children[i].click();
                addToCart();

                return true;
            }
        }

        var newSize = size - 0.5;
        selectSize(newSize);
        //console(newSize);

    } else {
        setTimeout("selectSize()", 250, size);
    }
}


function getSizeFromOption(callback) {
    chrome.storage.sync.get({
        selectedSize: defaultSize,
        selectedProductCode: 'code'
    }, function(items) {
        log("debug",items.selectedSize);
        log("debug",items.selectedProductCode);
        callback(items.selectedSize, items.selectedProductCode);
    });
}

function getCurrentPageProductCode() {
    //http://www.nike.com.hk/product/718763-505/detail.htm
    log("debug",window.location.href)
    
    var parser = document.createElement('a');
    parser.href = window.location.href;
    log("debug",parser.pathname); // => "/pathname/")

    var temp = parser.pathname.split("/");
    var productCode = temp[2];

    log("debug",productCode);
    return productCode;
}

// main call here
getSizeFromOption(function(selectedSize, selectedProductCode) {

    var startTime = new Date().getTime();
    log("info","Running")
    if ( selectedProductCode == "" || selectedProductCode == "code" )
    {
        log("info","Do not Select Product")
        selectSize(selectedSize)
        //setTimeout("selectSize()", 250, selectedSize);
    }
    else
    {
        log("info","Select Product")
        var productCode = getCurrentPageProductCode();
        
        log("info",productCode);
        log("info",selectedSize);
        log("info",selectedProductCode);
        if (productCode == selectedProductCode) {
            selectSize(selectedSize)
        }
    }
    var endTime = new Date().getTime();
    log("info","Used:" + (endTime - startTime) + " milliseconds");

})

// example to call the functoin each 250
//setTimeout("selectSize()", 250);
