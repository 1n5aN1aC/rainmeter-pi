//
// This Javascript file handles updating all the files on the index page
//

// This requests the current data via local json request.
// It then makes a callback to update() to handle the data.
function getTheJSON() {
	url = "/framework/http_status.py"
	if (window.wsgi == true) {
		url = "/status"
	}
	jQuery.getJSON(url, function(data) { update(data); } )
}

// update() handles actually updating the vales on the page from the json results
// This works by looping through each json element, and looking to see if there is
// a element with the same id as that.  If there is, it changes it's contents to
// the result of the json, after checking for several special cases.
function update(data) {
	$.each(data, function(k, v) {
		var theSpan = $('#' + k);
		//Rain-related ones need to be rounded to two decimal points.
		if (theSpan.attr('id') && theSpan.attr('id').indexOf("Rain") >= 0) {
			newVal = Math.round(v * 100) / 100
			theSpan.html(newVal)
		}
		//Humidity Sensors really only need the whole number.
		else if (theSpan.attr('id') && theSpan.attr('id').indexOf("Humid") >= 0) {
			theSpan.html( Math.round(v) )
		}
		//SYSTEM ones are jquery UI Progress bars.
		else if (theSpan.attr('id') && theSpan.attr('id').indexOf("SYSTEM") >= 0) {
			theSpan.progressbar({
				value: v
			});
		}
		//For the 'feels like' we only round to whole number
		else if (theSpan.attr('id') && theSpan.attr('id').indexOf("Feel") >= 0) {
			theSpan.html( Math.round(v) )
		}
		//Images we update the src= instead
		else if (theSpan.is("img")) {
			theSpan.attr("src", v);
		}
		//Everything else gets rounded to one decimal point.
		//We also make sure there are a decimal point, even when something is causing there to not be.
		else {
			number = Math.round(v * 10) / 10
			newlook = number + (number % 1 == 0 ? ".0" : "")
			theSpan.html(newlook)
		}
	});
	
	var date = new Date()
	minutes = (date.getMinutes() < 10 ? "0" : "") + date.getMinutes();
	hours = (date.getHours() > 12) ? date.getHours() - 12 : date.getHours();
	hours = ( hours == 0 ) ? 12 : hours;
	
	var theSpan = $('#DATE');
	theSpan.html(date.getMonth()+1 + "/" + date.getDate())
	
	var theSpan = $('#TIME');
	theSpan.html(hours + ":" + minutes)
}

// Handles when the user clicks the button to reset the rainfall.
function reset_rain() {
	url = "/framework/http_reset_rain.py"
	if (window.wsgi == true) {
		url = "/reset_rain"
	}
	$.ajax({
		url: url,
	});
}

// If the server responds to /status, we know wgsi is supported.
function check_wsgi() {
	$.ajax({
		type: "HEAD",
		url: "/status",
		success: function() {
			window.wsgi = true;
		},
		error: function() {
			window.wsgi = false;
		}
	});
}

document.addEventListener("DOMContentLoaded", function(event) {
	//Check if the webserver is set up to support wsgi (much faster)
	check_wsgi()
	//Update it now!
	getTheJSON()
	// Set up a permanent call to getTheJSON() every X seconds.
	window.setInterval(function(){  getTheJSON() }, 2000);
});