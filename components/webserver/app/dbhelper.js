var pg = require('pg');
var utils = require('./utils.js');

var getConfigsStmt = "SELECT id,sensorpin1,sensorpin2,lightpin,heatpin,humpin,daytemp,nighttemp,minhum,lightcontrol,heatcontrol,humcontrol,daystart,dayend,checkinterval FROM config;"
var getActiveConfigStmt = "SELECT id,sensorpin1,sensorpin2,lightpin,heatpin,humpin,daytemp,nighttemp,minhum,lightcontrol,heatcontrol,humcontrol,daystart,dayend,checkinterval FROM config WHERE active=TRUE;"
var getLogsStmt = "SELECT logtime,config,heating,light,hum,temp1,temp2,hum1,hum2 FROM log WHERE logtime>$1 AND logtime<$2;"

exports.logs = function(from, to, cb) {
	var conString = utils.getDBString();
	pg.connect(conString, function(err, client, done) {
		if(err) {
    		cb(err, null);
  		}

  		client.query(getLogsStmt, [from, to], function(err, result) {
  			done();
  			var logs = [];
  			var log;
  			for ( var i = 0; i < result.rows.length; i++) 
  				logs.push({log : result.rows[i]});
    		cb(err, logs);
  		});
	});
}

exports.configs = function(active, cb) {
	var conString = utils.getDBString();

	pg.connect(conString, function(err, client, done) {
		if(err) {
    		cb(err, null);
  		}

      var query = active != undefined && active ? getActiveConfigStmt : getConfigsStmt;
  		client.query(query, function(err, result) {
  			done();
  			var configs = [];
  			var config;
  			for ( var i = 0; i < result.rows.length; i++) 
  				configs.push({config : result.rows[i]});
    		cb(err, configs);
  		});
	});
}


