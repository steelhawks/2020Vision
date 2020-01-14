"use strict";

new Vue({
  el: '#app',
  template: '#main-template',
  data: {
    controls: {
        enable_camera: false,
        // enable_processing: false,
        camera_mode: 'R'
    }
  },
  mounted: function () {
    console.log('mounted');
  },
  methods: {
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
        self.controls.camera_mode = 'R';
        Socket.send(self.controls)
    },
    enableBall: function(){
        var self = this;
        self.controls.camera_mode = 'B';
        Socket.send(self.controls)
    },
    enableHex: function(){
        var self = this;
        self.controls.camera_mode = 'H'
        Socket.send(self.controls)
    },
    enableBay: function(){
        var self = this;
        self.controls.camera_mode = 'L'
        Socket.send(self.controls)
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