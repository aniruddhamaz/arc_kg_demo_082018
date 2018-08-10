var http = require('http');
var dt = require ('./myfirstmodule');
var fs = require ('fs');
var events = require ('events');
var eventEmitter = new events.EventEmitter () ;
var obj = JSON.parse(fs.readFileSync('techSummitDemo.json', 'utf8'));


//Create an event handler:
var myEventHandler = function () {
  console.log('I hear a scream!');
  console.log (obj);
}

//Assign the event handler to an event:
eventEmitter.on('scream', myEventHandler);

//Fire the 'scream' event:
eventEmitter.emit('scream');


http.createServer(function (req, res) {
  fs.readFile('techSummitDemo.html', function(err, data) {
    res.writeHead(200, {'Content-Type': 'text/html'});
    res.write(data);
    res.end();
  });

}).listen(8080); 
