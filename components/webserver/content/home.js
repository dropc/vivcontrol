$(function() {

	var tmpl, tdata = {};

	var initPage = function() {
		$.get("/home.html", function(d) {
			tmpl = d;
		});

		$.getJSON("/configs.json?active", function (d) {
			var config = d[0].config;

			if(config.lightcontrol == 1)
				config.lights = "On";
			else if(config.lightcontrol == 2)
				config.lights = "Auto";
			else
				config.lights = "Off";

			if(config.heatcontrol == 1)
				config.heating = "On";
			else if(config.heatcontrol == 2)
				config.heating = "Auto";
			else
				config.heating = "Off";

			if(config.humcontrol == 1)
				config.humidifier = "On";
			else if(config.humcontrol == 2)
				config.humidifier = "Auto";
			else
				config.humidifier = "Off";

			config.checkinterval = config.checkinterval/60;

			var min = config.daystart / 60;
			var hour = min / 60;
			min = min - (hour*60);
			if(min < 10){
				min = "0"+min
			}
			config.daytimestart = hour+":"+min;

			min = config.dayend / 60;
			hour = min / 60;
			min = min - (hour*60);
			if(min < 10){
				min = "0"+min
			}
			config.daytimeend = hour+":"+min;

			$.extend(tdata, config);
		});

		$(document).ajaxStop(function() {
			var renderedPage = Mustache.to_html(tmpl, tdata);
			$("body").html(renderedPage);
		});
	}();
});