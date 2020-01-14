import network as networktables
from web import tornado_server

def main():
    networktables.init()
    tornado_server.start()

if __name__ == '__main__':
    main()