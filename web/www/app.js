"use strict";

new Vue({
  el: '#app',
  template: '#main-template',
  data: {
    controls: {
        enable_camera: false,
        // enable_processing: false,
        camera_mode: 'R'
    },
    targets: [],
    color_profile: null
  },
  mounted: function () {
    console.log('mounted');
    var self = this;
  },
  methods: {
    onTargetUpdate: function(key, value, isNew) {
        //console.log(value);
        this.targets = value
    },
    updateColors: function() {
        var self = this;
        console.log(self.rgb)
        Socket.send({
            'profile':{
                'rgb': self.rgb,
                'hsv': self.hsv,
                'hsl': self.hsl
        }})
    },
    enableCamera: function () {
        var self = this;
        if(self.controls.enable_camera == false){
            self.controls.enable_camera = true;
        }
        else{
            self.controls.enable_camera = false;
        }
        Socket.send(self.controls)
    },
    enableRaw: function() {
        var self = this;
        self.controls.camera_mode = 'RAW';
        Socket.send({'controls':self.controls})

    },
    enableBall: function(){
        var self = this;
        self.controls.camera_mode = 'BALL';
        Socket.send({'controls':self.controls})
    },
    enableHex: function(){
        var self = this;
        self.controls.camera_mode = 'HEXAGON'
        Socket.send({'controls':self.controls})
    },
    enableBay: function(){
        var self = this;
        self.controls.camera_mode = 'BAY'
        Socket.send({'controls':self.controls})
    }
    // enableProcessing: function(){
    //     var self = this;
    //     if(self.controls.enable_processing == false){
    //       self.controls.enable_processing = true;
    //     }
    //     else{
    //       self.controls.enable_processing = false;
    //     }
    //     Socket.send(self.controls)
    // },

  }
});
