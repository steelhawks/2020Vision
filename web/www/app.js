"use strict";

new Vue({
  el: '#app',
  template: '#main-template',
  data: {
    controls: {
        enable_camera: false,
        // enable_processing: false,
        camera_mode: 'BAY'
    },
    targets: []
  },
  mounted: function () {
    console.log('mounted');
    var self = this;
    start_camera_stream("/processed/ws", "processed_image");
  },
  methods: {
    onTargetUpdate: function(key, value, isNew) {
        //console.log(value);
        this.targets = value
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
    },
    enableCalibrate: function(){
        var self = this;
        self.controls.camera_mode = 'CALIBRATE'
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
