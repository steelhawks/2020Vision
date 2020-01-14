"""
collect all known GStreamer methods here
"""

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

def appsrc():
    return 'appsrc'

def queue():
    return 'queue'

def videoconvert():
    return 'videoconvert'

def video_x_raw():
    return 'video/x-raw'

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
