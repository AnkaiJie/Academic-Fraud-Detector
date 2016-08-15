var express = require('express');
var app = express();
var port = process.env.PORT || 8000;
var PythonShell = require('python-shell')


app.get('/', function(req, res){

	pyshell = new PythonShell('testNode.py')

	pyshell.on('message', function(message){
		console.log(message);
	});

    res.sendFile(__dirname + '/index.html');
});

app.listen(port);
console.log("Miracles occur in port " + port);