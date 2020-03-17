#!/usr/bin/python3

# TODO:
# [X] Several definable thresholds
# [ ] Check for charging thresholds, and notify when fully charged.
# [X] Case statements?
# [X] Notification when charging and not charging

#import dbus
import notify2
from gi.repository import GLib
import dbus.mainloop.glib
from pydbus import SystemBus


# Change parameters here:
img_90_charge = 'battery-full-charging'
img_65_charge = 'battery-good-charging'
img_35_charge = 'battery-low-charging'
img_10_charge = 'battery-empty-charging'
img_90_discharge = 'battery-full'
img_65_discharge = 'battery-good'
img_35_discharge = 'battery-low'
img_10_discharge = 'battery-empty'
threshold_min = 20
threshold_minmin = 5


#dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
#bus = dbus.SystemBus()

#bat0_object = bus.get_object('org.freedesktop.UPower', 
#                      '/org/freedesktop/UPower/devices/battery_BAT0')
#bat0 = dbus.Interface(bat0_object, 'org.freedesktop.DBus.Properties')
#state = bat0.Get("org.freedesktop.UPower.Device", "State")
#percentage = bat0.Get("org.freedesktop.UPower.Device", "Percentage")
#time_to_full = bat0.Get("org.freedesktop.UPower.Device", "TimeToFull")
#time_to_empty = bat0.Get("org.freedesktop.UPower.Device", "TimeToEmpty")

bus = SystemBus()
bat0 = bus.get('.UPower', 'devices/battery_BAT0')
#print(bat0)
state = bat0.State
percentage = bat0.Percentage
time_to_full = bat0.TimeToFull
time_to_empty = bat0.TimeToEmpty
icon = bat0.IconName
print(bat0.WarningLevel) # 3=low, 4=critical
#bat0.PropertiesChanged.connect(print)
#bat0.onPropertiesChanged = print
help(bat0)
#loop = GLib.MainLoop()
#loop.run()


def sec_to_hours(seconds):
    if seconds >= 3600:
        a = str(seconds//3600)
        b = str((seconds%3600)//60)
        c = str((seconds%3600)%60)
        d = '{} Hours, {} Mins, {} Seconds'.format(a, b, c)
    else:
        b = str((seconds)//60)
        c = str((seconds)%60)
        d = '{} Minutes and {} Seconds'.format(b, c)
    return d


def send_notify(header, message, image):
    try:
        with open('/tmp/notify_battery.tmp', 'r') as num:
             nid = num.read()
    except FileNotFoundError:
        nid = 0

    notify2.init('Battery')
    n = notify2.Notification(header, message=str(message))
    n.set_hint_string('image-path', image)
    n.id = nid
    n.show()
    with open('/tmp/notify_battery.tmp', 'w') as num:
        num.write(str(n.id))


def img_select(percentage, state):
    if state == 1:
        image = {
            90 : img_90_charge,
            65 : img_65_charge, 
            35:  img_35_charge,
            10 : img_10_charge
                }
        return image.get(min(image.keys(), key=lambda x:abs(x-percentage)))
    else:
        image = {
            90 : img_90_discharge,
            65 : img_65_discharge,
            35 : img_35_discharge,
            10 : img_10_discharge
                }
        return image.get(min(image.keys(), key=lambda x:abs(x-percentage)))


#if state == 2: # DISCHARGING
#    send_notify('Discharging', sec_to_hours(time_to_empty) + ' to empty', img_select(percentage, state))
#if state == 1: # CHARGING
#    send_notify('Charging', sec_to_hours(time_to_full) + ' to full', img_select(percentage, state))
# if percentage <= threshold_min and percentage > threshold_minmin:
    # message = 'Battery is running low: ' + str(percentage) + ' %\n' + sec_to_hours(time_to_empty) + ' to empty'
    # send_notify('Battery low', message, img_35_discharge)
# if percentage <= threshold_minmin:
    # message = 'BATTERY IS RUNNING CRITICALLY LOW: ' + str(percentage) + ' %\n' + sec_to_hours(time_to_empty) + ' to empty'
    # send_notify('Battery low', message, img_10_discharge)

