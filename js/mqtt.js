var host = '10.0.0.21';	// hostname or IP address
var port = 9001;
var topic = 'home/#';		// topic to subscribe to
var useTLS = false;
var username = null;
var password = null;
var cleansession = true;
var mqtt;
var reconnectTimeout = 20000;

function MQTTconnect() {
	if (typeof path == "undefined") {
		path = '/mqtt';
	}
	mqtt = new Paho.MQTT.Client(host, port, path, "web_" + parseInt(Math.random() * 100, 10));
	var options = {
		timeout: 3,
		useSSL: useTLS,
		cleanSession: cleansession,
		onSuccess: onConnect,
		onFailure: function (message) {
			setTimeout(MQTTconnect, reconnectTimeout);
		}
	};

	mqtt.onConnectionLost = onConnectionLost;
	mqtt.onMessageArrived = onMessageArrived;

	if (username != null) {
		options.userName = username;
		options.password = password;
	}
	console.log("Host="+ host + ", port=" + port + ", path=" + path + " TLS = " + useTLS + " username=" + username + " password=" + password);
	mqtt.connect(options);
}

// Connection succeeded; subscribe to our topic
function onConnect() {
	mqtt.subscribe(topic, {qos: 0});
	$('#topic').val(topic);
}

// Connection failed; reconnect after timeout
function onConnectionLost(response) {
	setTimeout(MQTTconnect, reconnectTimeout);
};

// Message received; pass it on to be dealth with.
function onMessageArrived(message) {
	var topic = message.destinationName;
	var payload = message.payloadString;
	update(topic, payload);
};