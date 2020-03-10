#!/usr/bin/python3

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
#print(value)

def getval():
    with open('/home/stian/scripts/notify/temp.txt', 'r') as f:
    #with open('/sys/class/backlight/amdgpu_bl0/brightness', 'r') as f:
        raw = int(f.read())
    print('get')
    print(raw)
    return raw


def putval(value):
    if value > 0 and value < 255:
        with open('/home/stian/scripts/notify/temp.txt', 'w') as f:
#        with open('/sys/class/backlight/amdgpu_bl0/brightness', 'w') as f:
            f.write(str(value))


def calc():
    perc = round(getval()/2.55)
    return perc


def send_notify(message):
    try:
        with open('/tmp/brnottemp.txt', 'r') as num:
            nid = num.read()
    except FileNotFoundError:
        nid = 0

    notify2.init("Brightness")
    n = notify2.Notification('Brightness', message=str(message))
    n.id = nid
    n.show()
    with open('/tmp/brnottemp.txt', 'w') as num:
        num.write(str(n.id))


if args.up:
    a = round(getval()+25)
    putval(a)

if args.down:
    a = round(getval()-25)
    putval(a)

if args.value:
    percent = round(getval()/2.55)
    putval(round(value*2.55))
    send_notify(percent)
