import config

config.networktables_server_ip = '10.26.1.2'

# when using static ip for robot
#config.networktables_server_ip = '10.26.1.11'

config.video_source_number = 0
config.networktables_table = 'SmartDashboard'

config.gstreamer_bitrate = '3500000'
config.gstreamer_client_ip = '10.26.1.5'
config.gstreamer_client_port = '5805'
config.gstreamer_pipeline = 'appsrc ! videoconvert ! omxh264enc bitrate=%s ! video/x-h264, stream-format=(string)byte-stream ! h264parse ! rtph264pay ! udpsink host=%s port=%s' % (config.gstreamer_bitrate, config.gstreamer_client_ip, config.gstreamer_client_port)

# config.gstreamer_pipeline = 'appsrc ! videoconvert ! omxh265enc bitrate=%s ! video/x-h265, stream-format=(string)byte-stream ! h265parse ! rtph265pay ! udpsink host=%s port=%s' % (config.gstreamer_bitrate, config.gstreamer_client_ip, config.gstreamer_client_port)

tornado_server_port="8080"
