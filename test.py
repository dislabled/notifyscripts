#!/bin/python3
#from notify_send_py import NotifySendPy
#test = NotifySendPy().notify('test')
import notify2

try:
    with open('/tmp/brnottemp.txt', 'r') as num:
        nid = num.read()
except FileNotFoundError:
    nid = 0

notify2.init("Brightness")
n = notify2.Notification('Brightness', message='This shows the brightnessvalue')
n.id = nid
n.show()
with open('/tmp/brnottemp.txt', 'w') as num:
    num.write(str(n.id))
