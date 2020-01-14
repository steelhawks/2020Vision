import network as networktables


def connect(controller):

    dashboard = networktables.get()

    def on_enable_camera_change(table, key, value, isNew):
        print("Controller Update: '%s' -> %s" % (key, value))
        controller.enable_camera = value
        if not controller.enable_camera:
            controller.turn_camera_off

    # def on_enable_processing_change(table, key, value, isNew):
    #     print("Controller Update: '%s' -> %s" % (key, value))
    #     controller.enable_processing = value

    def on_camera_mode_change(table, key, value, isNew):
        print("Controller Update: '%s' -> %s" % (key, value))
        controller.camera_mode = value
    


    dashboard.addEntryListener(on_enable_camera_change,
                          immediateNotify=True,
                          key=networktables.keys.vision_enable_camera)

    dashboard.addEntryListener(on_camera_mode_change,
                          immediateNotify=True,
                          key=networktables.keys.vision_camera_mode)

    # dashboard.addEntryListener(on_enable_processing_change,
    #                       immediateNotify=True,
    #                       key=networktables.keys.vision_enable_processing)