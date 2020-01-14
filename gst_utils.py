"""
collect all known GStreamer methods here
"""

import logging

logger = logging.getLogger('gst')

def get_udp_streamer_pipeline2(host, port, bitrate):

    # config.gstreamer_pipeline = 'appsrc ! videoconvert ! omxh264enc bitrate=%s ! video/x-h264, stream-format=(string)byte-stream ! h264parse ! rtph264pay ! udpsink host=%s port=%s' % (config.gstreamer_bitrate, config.gstreamer_client_ip, config.gstreamer_client_port)

    pipeline = ' ! '.join( [appsrc(),
                            videoconvert(),
                            omxh264enc(bitrate=bitrate),
                            video_x264(byteStream=True),
                            h264parse(),
                            rtph264pay(),
                            udpsink(host,port)])
    logger.info(pipeline)
    return pipeline

def get_udp_sender(host, port):
    'appsrc ! queue ! videoconvert ! video/x-raw ! x264enc tune=zerolatency ! h264parse ! rtph264pay ! udpsink host="192.168.1.10" port="5000" sync=false'
    pipeline = ' ! '.join( [appsrc(),
                             queue(),
                             videoconvert(),
                             video_x_raw(),
                             x264enc(zerolatency=True),
                             h264parse(),
                             rtph264pay(),
                             udpsink(host,port)])

    print(pipeline)
    return pipeline

## PIPELINES
def omxh264enc(bitrate=None):
    if bitrate is not None:
        return 'omxh264enc bitrate=%s' % bitrate
    return 'omxh264enc'
    
def appsrc():
    return 'appsrc'

def queue():
    return 'queue'

def videoconvert():
    return 'videoconvert'

def video_x_raw():
    return 'video/x-raw'

def video_x264(byteStream=False):
    if byteStream: 
        return 'video/x-h264 stream-format=(string)byte-stream'
    return 'video/x-h264'

def x264enc(zerolatency=True):
    if zerolatency:
        return 'x264enc tune=zerolatency'
    return 'x264enc'

def h264parse():
    return 'h264parse'

def rtph264pay():
    return 'rtph264pay'

def udpsink(host, port, sync=False):
    if sync is False:
        return 'udpsink host="%s" port="%s" sync=false' % (host,port)
    return 'udpsink host="%s" port="%s"' % (host,port)
