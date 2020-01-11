import network as networktables
import json

def connect(profile):

    dashboard = networktables.get()

    def on_profile_change(table, key, value, isNew):
        print("ColorProfile Update: '%s' -> %s" % (key, value))

        p = json.loads(value)

        profile.red.min = int(p['red']['min'])
        profile.red.max = int(p['red']['max'])

        profile.blue.min = int(p['blue']['min'])
        profile.blue.max = int(p['blue']['max'])

        profile.green.min = int(p['green']['min'])
        profile.green.max = int(p['green']['max'])


    dashboard.addEntryListener(on_profile_change,
                          immediateNotify=True,
                          key=networktables.keys.vision_color_profile)



