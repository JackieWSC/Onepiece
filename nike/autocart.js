var defaultSize = "11";
var defaultSize1 = "7C";
var defaultSize2 = "8C";
var defaultSize3 = "9C";
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

function wait(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

function sleep(delay) {
    var start = new Date().getTime();
    while (new Date().getTime() < start + delay);
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
    // document.getElementsByClassName("size select-btn")[0].click();

    // select size
    var temp = document.getElementsByClassName("content-box2")[0];

    //var temp = document.getElementById("productSize");
    log("debug", "childElementCount:" + temp.childElementCount)


    if (temp.childElementCount > 1) {
        child_1 = temp.children[1]
        log("debug","children[1]:" + child_1.childElementCount)

        child_1_2 = child_1.children[1]
        log("debug","children[1-1]:" + child_1_2.className)

        child_1_2.click()
        log("debug","children[1-1] first child:" + child_1_2.firstChild.innerHTML)
    }

    // select size
    var temp2 = document.getElementsByClassName("content-box2")[0];

    //var temp = document.getElementById("productSize");
    log("debug", "!!!!childElementCount:" + temp2.childElementCount)


    if (temp2.childElementCount > 1) {
        child_1 = temp2.children[1]
        log("debug","children[1]:" + child_1.childElementCount)

        child_1_2 = child_1.children[1]
        log("debug","children[1-1]:" + child_1_2.className)

        child_1_2.click()
        log("debug","children[1-1] first child:" + child_1_2.firstChild.innerHTML)
    }

    //temp.children[1].click();
    if (temp != undefined) {
        for (var i = 0; i < temp.childElementCount; i++) {
            tempSize = temp.children[i].innerText.trim();
            log("debug","Available size:" + tempSize);

            if (tempSize == size || tempSize == defaultSize1 || tempSize == defaultSize2 || tempSize == defaultSize3 ) {
                temp.children[i].click();
                addToCart();

                return true;
            }
        }

        var newSize = size - 0.5;
        //selectSize(newSize);
        console.log("debug", "Size:" + newSize);

    }
    // else {
        // setTimeout("selectSize()", 250, size);
    // }
}


function getSizeFromOption(callback) {
    chrome.storage.sync.get({
        selectedSize: defaultSize,
        selectedProductCode: 'code'
    }, function(items) {
        log("debug","selectedSize:" + items.selectedSize);
        log("debug","selectedProductCode:" + items.selectedProductCode);
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
        log("info","Do not define Product Code")
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
