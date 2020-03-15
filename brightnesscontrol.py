#!/usr/bin/python3

# Add following rule to udev and add user to group video
# /etc/udev/rules.d/backlight.rules:
# ACTION=="add", SUBSYSTEM=="backlight", KERNEL=="%k", RUN+="/bin/chgrp video /sys/class/backlight/%k/brightness"
# ACTION=="add", SUBSYSTEM=="backlight", KERNEL=="%k", RUN+="/bin/chmod g+w /sys/class/backlight/%k/brightness"

import sys
import argparse
import notify2


parser = argparse.ArgumentParser()
parser.add_argument('-u', '--up', action='store_true', help='Turns brightness up by 10%')
parser.add_argument('-d', '--down', action='store_true', help='Turns brightness down by 10%')
parser.add_argument('-v', '--value', dest='value',
                    help='Set a brightness value between 0 - 100%', type=int, choices=range(0, 100))
args = parser.parse_args()
value = args.value


def getval():
    with open('/sys/class/backlight/amdgpu_bl0/brightness', 'r') as f:
        raw = int(f.read())
    return raw


def putval(value):
    if value > 255:
        value = 255
    if value > 0 and value <= 255:
        with open('/sys/class/backlight/amdgpu_bl0/brightness', 'w') as f:
            f.write(str(value))


def calc(raw):
    perc = round(raw/2.55)
    return perc


def send_notify(message):
    try:
        with open('/tmp/notify_brightness.tmp', 'r') as num:
            nid = num.read()
    except FileNotFoundError:
        nid = 0

    notify2.init("Brightness")
    n = notify2.Notification('Brightness', message=str(message))
    n.id = nid
    n.show()
    with open('/tmp/notify_brightness.tmp', 'w') as num:
        num.write(str(n.id))


if args.up:
    a = round(getval()+25)
    putval(a)
    send_notify(calc(getval()))

if args.down:
    a = round(getval()-25)
    putval(a)
    send_notify(calc(getval()))

if args.value:
    putval(round(value*2.55))
    send_notify(calc(getval()))

