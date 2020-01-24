#!/usr/bin/env python3

import network as networktables
from web import tornado_server

import logging
#initiate the top level logger

logger = logging.getLogger('app')


def main():
    tornado_server.start()

if __name__ == '__main__':

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(name)s] [%(levelname)-5.5s] %(message)s",
        handlers=[
            logging.StreamHandler()
        ]
    )
    main()
