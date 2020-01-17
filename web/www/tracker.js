"use strict";

var canvas = document.getElementById("canvas");
var ctx = canvas.getContext("2d");
var objs = []

var lastCalledTime;
var fps;

function requestAnimFrame() {

  if(!lastCalledTime) {
     lastCalledTime = Date.now();
     fps = 0;
     return;
  }
  var delta = (Date.now() - lastCalledTime)/1000;
  lastCalledTime = Date.now();
  fps = 1/delta;
}

function showFPS(){
    ctx.fillStyle = "Black";
    ctx.font      = "normal 16pt Arial";
    ctx.fillText(fps + " fps", 10, 26);
}

function draw(targets) {


    var offscreenCanvas = document.createElement('canvas');
    offscreenCanvas.width = canvas.width;
    offscreenCanvas.height = canvas.height;

    var octx = offscreenCanvas.getContext("2d");
    targets.forEach(function(target){
        octx.beginPath();
        octx.arc(target.xpos, target.ypos, target.radius, 0, Math.PI*2);
        octx.fillStyle = "#0095DD";
        octx.fill();
        octx.closePath();
    })

    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.drawImage(offscreenCanvas, 0, 0);
    showFPS()
    requestAnimFrame()

}

var socketOpen = false;

var connect = function() {
  // construct the websocket URI
	const loc = window.location;
	const protocol = loc.protocol === "https:" ? "wss:" : "ws:";
	const address = `${protocol}//${loc.host}/tracking/ws`;

	var socket = new WebSocket(address);
	if (socket) {
		socket.onopen = function() {
			console.info("Socket opened at " + address);
			socketOpen = true;
		};

		socket.onmessage = function(msg) {
			const data = JSON.parse(msg.data);
      if(data.hasOwnProperty('targets')){
          draw(data['targets'])
      }
		};

		socket.onclose = function() {
			if (socketOpen) {
				socketOpen = false;
				console.info("Socket closed");
			}
			// respawn the websocket
			setTimeout(connect, 600);
		};
	}
}

connect()
