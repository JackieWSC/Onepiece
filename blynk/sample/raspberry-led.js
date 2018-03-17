var Blynk = require('blynk-library');
var Gpio = require('onoff').Gpio;
var trigPin = new Gpio(8, 'out');
var echoPin = new Gpio(10, 'in', 'both');


var AUTH = '8b7365146c164bb88648e4569d4dec9a';

var blynk = new Blynk.Blynk(AUTH);

var v1 = new blynk.VirtualPin(1);
var v2 = new blynk.VirtualPin(1);
var v3 = new blynk.VirtualPin(1);
var v9 = new blynk.VirtualPin(9);

v1.on('write', function(param) {
  console.log('V1:', param[0]);
  
  if ( param[0] == '1') {
      trigPin.writeSync(1);
      trigPin.writeSync(0);
      echoPin.writeSync(1);

      v2.write(50);
  }

});

v9.on('read', function() {
  v9.write(new Date().getSeconds());
});



echoPin.watch(function(err, value) {
    console.log('echoPin:', value);
    v3.write(value);
});