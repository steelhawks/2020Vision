"use strict";

new Vue({
  el: '#app',
  template: '#main-template',
  data: {
    controls: {
        enable_camera: false,
        enable_processing: false,
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
        Socket.send({'controls': self.controls})
    }
  }
});