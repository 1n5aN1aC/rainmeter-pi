//
// This Javascript file handles updating all the files on the index page
//

// This requests the current data via local json request.
// It then makes a callback to update() to handle the data.
function getTheJSON() {
	jQuery.getJSON("/framework/get_update.py", function(data) { update(data); } )
}

// update() handles actually updating the vales on the page from the json results
// This works by looping through each json element, and looking to see if there is
// a element with the same id as that.  If there is, it changes it's contents to
// the result of the json, after checking for several special cases.
function update(data) {
	$.each(data, function(k, v) {
		var theSpan = $('#' + k);
		//Images we update the src= instead
		if (theSpan.is("img")) {
			theSpan.attr("src", v);
		}
		//Rain-related ones need to be rounded to two decimal points.
		else if (theSpan.attr('id') && theSpan.attr('id').includes("Rain")) {
			newVal = Math.round(v * 100) / 100
			theSpan.html(newVal)
		}
		//Wind-related ones need to be rounded to one decimal point.
		//else if (theSpan.attr('id') && theSpan.attr('id').includes("Wind")) {
		//	newVal = Math.round(v * 10) / 10
		//	theSpan.html(newVal)
		//}
		//SYSTEM ones are jquery UI Progress bars.
		else if (theSpan.attr('id') && theSpan.attr('id').includes("SYSTEM")) {
			$( "#" + k ).progressbar({
				value: v
			});
		}
		else if (theSpan.attr('id') && theSpan.attr('id').includes("SYSTEM")) {
			$( "#" + k ).progressbar({
				value: v
			});
		}
		//Everything else gets rounded to the nearest whole number
		else {
			theSpan.html(Math.round(v * 10) / 10)
		}
	});
}

function reset_rain() {
	$.ajax({
		url: "/framework/reset_rain.py",
	});
}


//Update it now!
getTheJSON()
// Set up a permanent call to getTheJSON() every X seconds.
window.setInterval(function(){  getTheJSON() }, 5000);