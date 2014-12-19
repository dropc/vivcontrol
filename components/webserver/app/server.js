var fs = require('fs');
var express = require('express');
var bodyParser = require('body-parser');
var dbhelper = require('./dbhelper.js');
var utils = require('./utils.js');

var app = express();

app.use(express.static(__dirname +"/../content"));
app.use(bodyParser.urlencoded({ extended: true }));

app.get('/configs.json', getConfigs);
app.post('/configs.json', saveConfig);
app.get('/logs.json', getLogs);
app.get('/page/:page', servePage)
app.get('*', notFound);

app.listen(8080);

function servePage(req, res) {
	var page = req.params.page;

	fs.readFile('../content/basic.html', function(err, contents) {
		if(err) {
			utils.sendFailureHTML(res, 500, "Template basic.html not found");
			return;
		}

		contents = contents.toString('utf8');
		contents = contents.replace('{{PAGENAME}}', page);
		utils.sendSuccessHTML(res, contents);
	});
}

function getConfigs(req, res) {
	var active = req.query.active != undefined;
	dbhelper.configs(active, function(err, result) {
		if(err) {
    		utils.sendFailure(res, null, err);
    	}
		utils.sendSuccess(res, result);
	});
}

function saveConfig(req, res) {
	var config = {};
	console.log(req.body);

	config.id = req.body.id;

	if(req.body.lights=="On")
		config.lightcontrol = 1;
	else if(req.body.lights=="Off")
		config.lightcontrol = 0;
	else 
		config.lightcontrol = 2;

	if(req.body.heating=="On")
		config.heatcontrol = 1;
	else if(req.body.heating=="Off")
		config.heatcontrol = 0;
	else 
		config.heatcontrol = 2;

	if(req.body.humidifier=="On")
		config.humcontrol = 1;
	else if(req.body.humidifier=="Off")
		config.humcontrol = 0;
	else 
		config.humcontrol = 2;

	config.lightpin = req.body.lightpin;
	config.heatpin = req.body.heatpin;
	config.humpin = req.body.humpin;
	config.sensorpin1 = req.body.sensorpin1;
	config.sensorpin2 = req.body.sensorpin2;
	config.daytemp = req.body.daytemp;
	config.nighttemp = req.body.nighttemp;
	config.minhum = req.body.minhum;

	var tmp = req.body.daytimestart.split(":");
	config.daystart = parseInt(tmp[0])*3600 + parseInt(tmp[1])*60;

	tmp = req.body.daytimeend.split(":");
	config.dayend =  parseInt(tmp[0])*3600 + parseInt(tmp[1])*60;
	
	config.checkinterval = req.body.checkinterval * 60;

	console.log(config);

	res.redirect("/page/home");
}

function getLogs(req, res) {
	var timeFrom = req.query.from;
	var timeTo = req.query.to;

	timeFrom = timeFrom != undefined && timeFrom ? timeFrom :  (new Date(0)).toISOString();
	timeTo = timeTo != undefined && timeTo ? timeTo : (new Date()).toISOString();

	timeFrom = utils.getEpochInSec(timeFrom);
	timeTo = utils.getEpochInSec(timeTo);

	dbhelper.logs(timeFrom, timeTo, function(err, result) {
		if(err) {
    		utils.sendFailure(res, null, err);
    	}
		utils.sendSuccess(res, result);
	});
}

function notFound(req, res) {
	utils.sendFailure(res, 404, "The requested resource does not exist.");
}


