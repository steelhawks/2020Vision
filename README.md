# 2020Vision

Vision processing code written in python3 for 2020 FRC Competition (detects outer port, powercells, and loading bay)

### dependencies
 - pynetworktables
 - cv2

### notes
 if running on the jetson nano, no virtualenv is required. If virtualenv is used, create with global site-packages enabled to pull in openCV2
 ```
  virtualenv -p python3 --system-site-packages 2020Vision
 ```

### running the program
```
python main.py
```

out = cv2.VideoWriter( gst_utils.get_udp_sender(host='192.168.1.10', port='5000'), 0,25.0,(640,480))
