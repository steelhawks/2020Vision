function new_web_socket(uri_path) {
  var protocol = 'ws:';
  if (window.location.protocol === 'https:') {
      protocol = 'wss:';
  }
  var host = window.location.host;
  var url = protocol + '//' + host + uri_path;
  console.log(url);
  var ws = new WebSocket(url);
  return ws;
}


var start_camera_stream = function( websocket_source, target) {

  var image = document.getElementById(target)
  ws_imagestream = new_web_socket( websocket_source);

  time_0 = (new Date()).getTime();
  counter = 0;

  update_fps = function() {
      counter += 1;
      if ((counter % 5) == 0) {
          tdif = (new Date()).getTime() - time_0;
          time_0 = (new Date()).getTime();
          fps = Math.round(5 * 1.0 / (tdif / 1000.0));
          $(document).ready(function(){
            $('#actual').text(fps);
          });
          
      }
  }


  ws_imagestream.onmessage = function(e) {
      if (e.data instanceof Blob) {
          update_fps()
          image.src = URL.createObjectURL(e.data);
          image.onload = function() {
              URL.revokeObjectURL(image.src);
          }
      }
  }

  ws_imagestream.onopen = function() {
      console.log('connected ws_imagestream...');
      ws_imagestream.send("open feed")
  };
  ws_imagestream.onclose = function() {
      console.log('closed feed ');
  };
};
