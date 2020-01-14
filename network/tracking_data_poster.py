import network as networktables

def send_tracking(data):    
    dashboard = networktables.get()
    dashboard.putValue(networktables.keys.vision_target_data, json.dumps(data))
