exports.getEpochInSec = function(time) {
	return parseInt(Date.parse(time)/1000);
}

exports.getDBString = function(host, port, dbname, dbuser, dbpass) {
	host = host == undefined ? "localhost" : host;
	port = port == undefined ? "5432" : port;
	dbname = dbname == undefined ? "vivcontrol" : dbname;
	dbuser = dbuser == undefined ? "postgres" : dbuser;

	if(dbpass == undefined)
		return "postgres://"+dbuser+"@"+host+":"+port+"/"+dbname;
	else
		return "postgres://"+dbuser+":"+dbpass+"@"+host+":"+port+"/"+dbname;
}

exports.sendSuccess = function(res, data) {
	res.writeHead(200, {"Content-Type": "application/json"});
	res.end(JSON.stringify(data) + "\n");
}

exports.sendFailure = function(res, code, err) {
	code = code != undefined && code ? code : "500";
	res.writeHead(code, { "Content-Type" : "application/json" });
	res.end(JSON.stringify(err) + "\n");
}

exports.sendSuccessHTML = function(res, data) {
	res.writeHead(200, {"Content-Type": "text/html"});
	res.end(data + "\n");
}

exports.sendFailureHTML = function(res, code, err) {
	code = code != undefined && code ? code : "500";
	res.writeHead(code, { "Content-Type" : "text/html" });
	res.end(err + "\n");
}
