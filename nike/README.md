# nike
## chrome-extension to select the shoes in nike store and add to cart

* anifest.json 
  ** define the plugin name, version, config

* popup.html
  ** setting page

* autocart.js
  ** add the product to the cart with defined size
  ** if the defined size sold out, it will try with next smaller size
  ** e.g try 11 first, then 10.5 and next is 10

* transaction.js 
  ** auto select the validate code input

* redirect.js