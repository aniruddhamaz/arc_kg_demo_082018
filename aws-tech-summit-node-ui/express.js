var http = require('http');
var express = require('express');
var dt = require ('./myfirstmodule');
var fs = require ('fs');
var events = require ('events');
var eventEmitter = new events.EventEmitter () ;
var obj = JSON.parse(fs.readFileSync('techSummitDemo.json', 'utf8'));


var app = express();

//Create an event handler:
var myEventHandler = function () {
  console.log('I hear a scream!');
  console.log (obj);
}

//Assign the event handler to an event:
eventEmitter.on('scream', myEventHandler);

//Fire the 'scream' event:
eventEmitter.emit('scream');

app.get('/', function(req, res) {
    res.end('You\'re in reception');
});

app.get('/ddstatus', function(req, res) {
    var names = ['Robert', 'Jack', 'David'];
    var measuredValues = JSON.parse(fs.readFileSync('./techSummitDemo.json', 'utf8'));
    console.log('Sending device defender contents !');
    console.log('Object is : ' + JSON.stringify(measuredValues));
    res.render('techSummitDemo.ejs', {pcr: JSON.stringify(measuredValues), counter : 4});
});

app.listen(8080);
