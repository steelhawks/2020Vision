import cv2
import config
import time

from imagezmq import imagezmq
from processing import filters

def main():

    cap = cv2.VideoCapture(config.video_source_number)

    sender = imagezmq.ImageSender(connect_to="tcp://{}:5555".format('192.168.1.25'))

    while(True):

        _, frame = cap.read()

        frame = filters.resize(frame, 640, 480, interpolation=cv2.INTER_CUBIC)

        sender.send_image('testImage', frame)

if __name__ == '__main__':
    main()
