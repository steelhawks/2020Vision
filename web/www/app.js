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
    rgb: {
        red: {
            min: 0,
            max: 255
        },
        green: {
            min: 0,
            max: 255
        },
        blue: {
            min: 0,
            max: 255
        }
    }
  },
  mounted: function () {
    console.log('mounted');
  },
  methods: {

    updateColors: function() {
        var self = this;
        console.log(self.rgb)
        Socket.send({
                'rgb': self.rgb
        })
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
        Socket.send({
            'controls': self.controls
        })
    },
    enableBall: function(){
        var self = this;
        self.controls.camera_mode = 'BALL';
        Socket.send({'controls':self.controls})
    },
    enableHex: function(){
        var self = this;
        self.controls.camera_mode = 'HEXAGON'
        Socket.send(self.controls)
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