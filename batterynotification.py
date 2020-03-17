#!/usr/bin/python3

# TODO:
# * Use pydbus instead of notify2?
# * Thresholds Notification
# Thresholds needs to be set in /etc/UPower/UPower.conf
#


import notify2
from gi.repository import GLib
from pydbus import SystemBus


bus = SystemBus()
bat0 = bus.get('.UPower', 'devices/battery_BAT0')
icon = bat0.IconName
warning = bat0.WarningLevel # 3=low, 4=critical
help(bat0)


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


def event(useless1, list, useless2):
    if list.get('State') == 2: # DISCHARGING
        send_notify('Discharging', sec_to_hours(list.get('TimeToEmpty')) + ' to empty', list.get('IconName'))
    if list.get('State') == 1: # CHARGING
        send_notify('Charging', sec_to_hours(list.get('TimeToFull')) + ' to full', list.get('IconName'))

bat0.PropertiesChanged.connect(event)
loop = GLib.MainLoop()
loop.run()


# if percentage <= threshold_min and percentage > threshold_minmin:
    # message = 'Battery is running low: ' + str(percentage) + ' %\n' + sec_to_hours(time_to_empty) + ' to empty'
    # send_notify('Battery low', message, img_35_discharge)
# if percentage <= threshold_minmin:
    # message = 'BATTERY IS RUNNING CRITICALLY LOW: ' + str(percentage) + ' %\n' + sec_to_hours(time_to_empty) + ' to empty'
    # send_notify('Battery low', message, img_10_discharge)

