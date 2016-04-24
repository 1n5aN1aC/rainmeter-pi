// Initial document ready function
//registers listeners / timers
$(document).ready(function() {
	updateTime()
	defineBandwidth()
	
	setInterval(function(){updateTime()}, 10000);
});

var monthNames = ["January", "February", "March", "April", "May", "June",
	"July", "August", "September", "October", "November", "December"];

// Updates the Time & Date
function updateTime() {
	var date = new Date()
	minutes = (date.getMinutes() < 10 ? "0" : "") + date.getMinutes();
	hours = (date.getHours() > 12) ? date.getHours() - 12 : date.getHours();
	hours = ( hours == 0 ) ? 12 : hours;
	
	var theDate = $('date');
	theDate.html(monthNames[date.getMonth()] + "&nbsp;&nbsp;" + date.getDate())
	
	var thetime = $('time');
	thetime.html(hours + ":" + minutes)
}

function attemptFullscreen() {
	var elem = document.getElementById("bodyzone");
	if (elem.requestFullscreen) {
	  elem.requestFullscreen();
	} else if (elem.msRequestFullscreen) {
	  elem.msRequestFullscreen();
	} else if (elem.mozRequestFullScreen) {
	  elem.mozRequestFullScreen();
	} else if (elem.webkitRequestFullscreen) {
	  elem.webkitRequestFullscreen();
	}
}

// Defines the Highcharts for site bandwidth
function defineBandwidth() {
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
            data: [21],
            dataLabels: {
                format: '<div style="text-align:center"><span style="font-size:38px;color:' +
                    ((Highcharts.theme && Highcharts.theme.contrastTextColor) || 'white') + '">{y}</span><br/>' +
                       '<span style="font-size:12px;color:silver;top:-15px;position:relative;">mph</span></div>'
            },
		}]
	});
}