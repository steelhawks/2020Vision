"use strict";

new Vue({
  el: '#app',
  template: '#main-template',
  data: {
    controls: {
        enable_camera: false,
        enable_processing: false,
        camera_mode: 'R'
    }
  },
  mounted: function () {
    console.log('mounted');
  },
  methods: {
    enableCamera: function () {
        var self = this;
        self.controls.enable_camera = self.controls.enable_camera
        Socket.send(self.controls)
    }
  }
});