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


var start_camera_stream = function() {

  time_0 = (new Date()).getTime();
  counter = 0;

  update_fps = function() {
      counter += 1;
      if ((counter % 5) == 0) {
          tdif = (new Date()).getTime() - time_0;
          time_0 = (new Date()).getTime();
          fps = Math.round(5 * 1.0 / (tdif / 1000.0));
          $('#actual').text(fps);
      }
  }

  ws_imagestream = new_web_socket('/camera/ws');

  ws_imagestream.onmessage = function(e) {
      if (e.data instanceof Blob) {
          update_fps()
          image.src = URL.createObjectURL(e.data);
          image.onload = function() {
              URL.revokeObjectURL(image.src);
          }
      }
      if (window.stream_mode == "get") {
          setTimeout(function(){ws_imagestream.send('?')}, interval);
      }
  }

  ws_imagestream.onopen = function() {
      console.log('connected ws_imagestream...');
      ws_imagestream.send('?');
  };
  ws_imagestream.onclose = function() {
      console.log('closed ws_imagestream');
  };
  //ws_imagestream.send('?');
};

new Vue({
  el: '#app',
  template: '#main-template',
  data: {
    color_modes: ['rgb', 'hsv', 'hsl'],
    color_profiles: null,
    selected_color_mode: null,
    selected_profile: null,
    controls_ws: null,
    apply_mask: false
  },
  computed: {
    "values": function(){
      let selected_profile = this.selected_profile;
      let selected_color_mode = this.selected_color_mode;

      if( selected_profile && selected_color_mode ){
        if( selected_color_mode == 'rgb') {
          return [
            {
              name: 'R',
              range: selected_profile.rgb.r
            },
            {
              name: 'G',
              range: selected_profile.rgb.g
            },
            {
              name: 'B',
              range: selected_profile.rgb.b
            }
          ]
        }
        if( selected_color_mode == 'hsl') {
          return [
            {
              name: 'H',
              range: selected_profile.hsl.h
            },
            {
              name: 'S',
              range: selected_profile.hsl.s
            },
            {
              name: 'V',
              range: selected_profile.hsl.l
            }
          ]
        }
        if( selected_color_mode == 'hsv') {
          return [
            {
              name: 'H',
              range: selected_profile.hsv.h
            },
            {
              name: 'S',
              range: selected_profile.hsv.s
            },
            {
              name: 'V',
              range: selected_profile.hsv.v
            }
          ]
        }
      }
      return []
    }
  },
  mounted: function () {
    var self = this;
    self.controls_ws = new_web_socket('/dashboard/ws');
    self.controls_ws.onmessage = function(msg) {
      var data = JSON.parse(msg.data)
      console.log(data);
      if(data.hasOwnProperty('color_profiles')){
        self.color_profiles = data.color_profiles;
        if( self.selected_profile) {
          self.selected_profile = self.color_profiles[self.selected_profile.camera_mode]
        }
      }
      //self.$forceUpdate();
    }
    start_camera_stream();

  },
  methods: {
    changeProfile: function(profile) {
      this.selected_profile = profile;
      ws_imagestream.send(JSON.stringify({camera_mode:this.selected_profile.camera_mode,
                                          color_mode: this.selected_color_mode,
                                          apply_mask: this.apply_mask}));
    },
    changeApplyMask: function() {
      ws_imagestream.send(JSON.stringify({camera_mode:this.selected_profile.camera_mode,
                                          color_mode: this.selected_color_mode,
                                          apply_mask: this.apply_mask}));
    },
    changeColorMode: function(color_mode) {
      this.selected_color_mode = color_mode
      ws_imagestream.send(JSON.stringify({camera_mode:this.selected_profile.camera_mode,
                                          color_mode: this.selected_color_mode,
                                          apply_mask: this.apply_mask}));
    },
    updateColors: function() {
        var self = this;
        console.log(self.color_profiles)
        self.controls_ws.send(JSON.stringify({'color_profile': self.selected_profile}))
    },
    saveProfile: function() {
        var self = this;
        self.controls_ws.send(JSON.stringify({'color_profile': self.selected_profile,
                                              'save': true}))
    },
    resetProfile: function() {
        var self = this;
        self.controls_ws.send(JSON.stringify({'color_profile': self.selected_profile,
                                              'reset': true}))
    }
  }
});
