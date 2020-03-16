#!/usr/bin/python3



import sys
import argparse
import notify2
import pulsectl
import os

parser = argparse.ArgumentParser()
parser.add_argument('-u', '--up', action='store_true', help='Turns Volume uo by 5%')
parser.add_argument('-d', '--down', action='store_true', help='Turns Volume down by 5%')
parser.add_argument('-m', '--mute', action='store_true', help='Toggle Mute Volume')
parser.add_argument('-v', '--value', dest='value',
                    help='Set volume to a value between 0 - 100%', type=int, choices=range(0, 100))
args = parser.parse_args()
value = args.value

p = pulsectl.Pulse('volume-control')


def get_active_sink():
    default = p.server_info().default_sink_name
    for sink in p.sink_list():
        if default in str(sink):
            return sink


def change_volume(val):
    sink = get_active_sink()
    p.volume_change_all_chans(sink, val)
    output = int(p.volume_get_all_chans(sink) * 100)
    file = 'volume.wav'
    os.system('aplay ' + file)
    return output


def set_volume(val):
    sink = get_active_sink()
    p.volume_set_all_chans(sink, val)


def toggle_mute():
    sink = get_active_sink()
    if sink.mute == 0:
        p.mute(sink, mute=True)
        msg = 'Mute'
    else:
        p.mute(sink, mute=False)
        msg = 'UnMute'
    return msg


def send_notify(message):
    try:
        with open('/tmp/notify_vil.tmp', 'r') as num:
            nid = num.read()
    except FileNotFoundError:
        nid = 0

    notify2.init('Volume')
    n = notify2.Notification('Volume', message=str(message))
    n.id = nid
    n.show()
    with open('/tmp/notify_vol.tmp', 'w') as num:
        num.write(str(n.id))


if args.up:
    send_notify(str(change_volume(0.05)) + ' %')

if args.down:
    send_notify(str(change_volume(-0.05)) + ' %')

if args.mute:
    send_notify(toggle_mute())

if args.value:
    a = value / 100
    set_volume(a)
