#!/usr/bin/python3

# TODO:
# [ ] Several definable thresholds
# [ ] Check for charging thresholds, and notify when fully charged.
# [ ] Notification when charging and not charging

import dbus
import notify2
import datetime

# Change images here:
img_charge = 'battery-full-charging'
img_discharge = 'battery-low'
img_full = 'battery-full'
img_low = 'battery-low'
img_crit = 'battery-empty'



bus = dbus.SystemBus()
bat0_object = bus.get_object('org.freedesktop.UPower', 
                      '/org/freedesktop/UPower/devices/battery_BAT0')
bat0 = dbus.Interface(bat0_object, 'org.freedesktop.DBus.Properties')
state = bat0.Get("org.freedesktop.UPower.Device", "State")
percentage = bat0.Get("org.freedesktop.UPower.Device", "Percentage")
time_to_full = bat0.Get("org.freedesktop.UPower.Device", "TimeToFull")
time_to_empty = bat0.Get("org.freedesktop.UPower.Device", "TimeToEmpty")


def sec_to_hours(seconds):
    a=str(seconds//3600)
    b=str((seconds%3600)//60)
    c=str((seconds%3600)%60)
    d=["{} hours {} mins {} seconds".format(a, b, c)]
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


if state == 2: # DISCHARGING
    send_notify('Discharging', sec_to_hours(time_to_empty), img_discharge)
if state == 1: # CHARGING
    send_notify('Charging', sec_to_hours(time_to_empty), img_charge)
