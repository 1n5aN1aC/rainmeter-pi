//
// This Javascript file handles updating all the data on the index page
//

// Initial document ready function
//  registers listeners / timers
$(document).ready(function() {
	// Get the data for the first time!
	getTheJSON()
	// Update the clock for the first time!
	updateTime()
	// Create the windSpeed meter.
	defineWindSpeed()
	
	
	// Update the clock every 10 seconds
	setInterval(function(){updateTime()}, 10000);
	// Set up a permanent call to getTheJSON() every X seconds.
	window.setInterval(function(){  getTheJSON() }, 2000);
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

// This requests the current data via local json request.
//  It then makes a callback to update() to handle the data when it arrives.
function getTheJSON() {
	jQuery.getJSON("/status", function(data) { update(data); } )
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
			newVal = v.toFixed(2)
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
			number = v.toFixed(1)
			theSpan.html(number)
		}
	});
	
	var date = new Date()
	minutes = (date.getMinutes() < 10 ? "0" : "") + date.getMinutes();
	hours = (date.getHours() > 12) ? date.getHours() - 12 : date.getHours();
	hours = ( hours == 0 ) ? 12 : hours;
}

// Handles when the user clicks the button to reset the rainfall.
//  Yes.  We don't even check the result...
function reset_rain() {
	$.ajax({
		url: "/reset_rain",
	});
}

// Defines the Highcharts for Wind Speed
function defineWindSpeed() {
	info = new Highcharts.Chart({
		chart: {
			type: 'solidgauge',
			renderTo: 'speed',
			margin: [0, 0, 0, 0],
			backgroundColor: null,
			plotBackgroundColor: 'none',
		},
		
		title: null,
		
		pane: {
            center: ['50%', '85%'],
            size: '140%',
            startAngle: -90,
            endAngle: 90,
            background: {
                backgroundColor: (Highcharts.theme && Highcharts.theme.background2) || '#EEE',
                innerRadius: '60%',
                outerRadius: '100%',
                shape: 'arc'
            }
        },
		
		credits: {
            enabled: false
        },

		tooltip: {
			enabled: false
		},
		
		// the value axis
        yAxis: {
			min: 0,
            max: 60,
			minColor: "#B2C831",
			maxColor: "#FA1D2D",
			tickInterval: 60,
            lineWidth: 0,
            minorTickInterval: null,
            tickPixelInterval: 400,
            tickWidth: 0,
            title: null,
            labels: {
                y: 16
            }
        },
		
		plotOptions: {
            solidgauge: {
                dataLabels: {
                    y: 35,
                    borderWidth: 0,
                    useHTML: true
                }
            }
        },
		
		series: [{
			name: 'Speed',
            data: [99],
            dataLabels: {
                format: '<div style="text-align:center"><span style="font-size:38px;color:' +
                    ((Highcharts.theme && Highcharts.theme.contrastTextColor) || 'white') + '">{y}</span><br/>' +
                       '<span style="font-size:12px;color:silver;top:-15px;position:relative;">mph</span></div>'
            },
		}]
	});
}