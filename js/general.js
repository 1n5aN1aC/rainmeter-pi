//
// This Javascript file handles updating all the data on the index page
//

// Initial document ready function
//  registers listeners / timers
$(document).ready(function() {
	// Update the clock for the first time!
	updateTime()
	// get DatMQTT running!
	MQTTconnect()
	
	// Update the clock every 10 seconds
	setInterval(function(){ updateTime() }, 10000);
	//Update the radar every 14 minutes.
	setInterval(function(){ update_radar() }, 840000);
});

// Updates the Time & Date
var monthNames = ["January", "February", "March", "April", "May", "June",
	"July", "August", "September", "October", "November", "December"];
function updateTime() {
	var date = new Date()
	minutes = (date.getMinutes() < 10 ? "0" : "") + date.getMinutes();
	hours = (date.getHours() > 12) ? date.getHours() - 12 : date.getHours();
	hours = ( hours == 0 ) ? 12 : hours;
	
	var theDate = $('#date');
	theDate.html(monthNames[date.getMonth()] + "&nbsp;&nbsp;" + date.getDate())
	
	var thetime = $('#time');
	thetime.html(hours + ":" + minutes)
}

// Attempts to make the webapp fullscreen
//  Will toggle it off if already fullscreen
function attemptFullscreen() {
	if (!document.fullscreenElement && !document.mozFullScreenElement && !document.webkitFullscreenElement && !document.msFullscreenElement ) {
		if (document.documentElement.requestFullscreen) {
			document.documentElement.requestFullscreen();
		} else if (document.documentElement.msRequestFullscreen) {
			document.documentElement.msRequestFullscreen();
		} else if (document.documentElement.mozRequestFullScreen) {
			document.documentElement.mozRequestFullScreen();
		} else if (document.documentElement.webkitRequestFullscreen) {
			document.documentElement.webkitRequestFullscreen(Element.ALLOW_KEYBOARD_INPUT);
		}
	} else {
		if (document.exitFullscreen) {
			document.exitFullscreen();
		} else if (document.msExitFullscreen) {
			document.msExitFullscreen();
		} else if (document.mozCancelFullScreen) {
			document.mozCancelFullScreen();
		} else if (document.webkitExitFullscreen) {
			document.webkitExitFullscreen();
		}
	}
}

// update() handles actually updating the vales on the page from the json results
// This works by looping through each json element, and looking to see if there is
// a element with the same id as that.  If there is, it changes it's contents to
// the result of the json, after checking for several special cases.
function update(key, v) {
	type = key.split('/').pop().trim(); //last octave
	//Rain-related ones need to be rounded to two decimal points.
	if (type === "temp") {
		v = parseFloat(v)
		v = v.toFixed(1)
	}
	//Humidity Sensors really only need the whole number.
	else if (type === "humid") {
		v = parseFloat(v)
		v = Math.round(v)
	}
	
	//Wind speed
	if (key === "home/roof/weather/wind") {
		v = parseInt(v)
		$("#OUT_Wind").text(v)
	}
	else if (key === "home/roof/weather/wind/avg") {
		v = parseFloat(v)
		v = v.toFixed(1)
		$("#OUT_Wind_Avg").text(v)
	}
	else if (key === "home/roof/weather/wind/gust") {
		v = parseFloat(v)
		v = Math.round(v)
		$("#OUT_Wind_Gust").text(v)
	}
	else if (key === "home/roof/weather/wind/max") {
		v = parseFloat(v)
		v = Math.round(v)
		$("#OUT_Wind_Max").text(v)
	}
	//roof
	else if (key === "home/roof/weather/temp") {
		$("#OUT_Temp").text(v)
	}
	else if (key === "home/roof/weather/humid") {
		$("#OUT_Humid").text(v)
	}
	//living room
	else if (key === "home/living/micro/temp") {
		$("#IN_Temp").text(v)
	}
	else if (key === "home/living/micro/humid") {
		$("#IN_Humid").text(v)
	}
	//attic
	else if (key === "home/attic/controller/temp") {
		$("#ATTIC_Temp").text(v)
	}
	else if (key === "home/attic/controller/humid") {
		$("#ATTIC_Humid").text(v)
	}
	//rain
	else if (key === "home/roof/weather/rain/24hour") {
		$("#OUT_Rain_Last_24h").text(v)
	}
	else if (key === "home/roof/weather/rain/day") {
		$("#OUT_Rain_Today").text(v)
	}
	else if (key === "home/roof/weather/rain/alltime") {
		$("#OUT_Rain_Since_Reset").text(v)
	}
	//Images we update the src= instead
	else if (key === "home/nodered/weather/icon") {
		$("#NOW_URL").attr("src", v);
	}
	//forecast
	else if (key === "home/nodered/weather/feels") {
		v = parseFloat(v)
		v = Math.round(v)
		$("#NOW_Feel").text(v)
	}
	else if (key === "home/nodered/weather/high") {
		$("#NOW_Feel_High").text(v)
	}
	else if (key === "home/nodered/weather/low") {
		$("#NOW_Feel_Low").text(v)
	}
}

//We have to set it to something else before setting it back
//Otherwise it won't actually update
function update_radar() {
	$("#Radar_Holder").html("Reloading...");
	setTimeout(function(){ really_update_radar() }, 1000);
}
//Now we REALLY update the radar.
function really_update_radar() {
	$("#Radar_Holder").html("<img id='Radar_Img' src='http://api.wunderground.com/api/e8b292334779aa96/animatedradar/image.gif?centerlat=44.9&centerlon=-123.3&radius=40&newmaps=1&timelabel=1&timelabel.y=10&num=15&delay=50&width=481&height=242&nonce=" + new Date().getTime() + "'/>");
}

// Handles when the user clicks the button to reset the rainfall.
function reset_rain() {
	console.log("Clicked!")
	message = new Paho.MQTT.Message("RESET_TAP");
	message.destinationName = "home/roof/weather/rain/reset";
	mqtt.send(message);
}