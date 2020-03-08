#!/usr/bin/env bash

# You can call this script like this:
# $ ./brightnessControl.sh up
# $ ./brightnessControl.sh down

# Script inspired by these wonderful people:
# https://github.com/dastorm/volume-notification-dunst/blob/master/volume.sh
# https://gist.github.com/sebastiencs/5d7227f388d93374cebdf72e783fbd6a

function get_brightness {
  xbacklight -get | cut -d '.' -f 1
}

function send_notification {
  icon="notification-display-brightness-medium"
  brightness=$(get_brightness)
  printf -v brightnesspad "% 5d" $brightness
 # Make the bar with the special character ─ (it's not dash -)
  # https://en.wikipedia.org/wiki/Box-drawing_character
  bar=$(seq -s "―" 0 $((brightness / 5)) | tr -d '\n' | sed 's/[0-9]//g'; seq -s " " $((brightness / 5)) 20 | tr -d '\n' | sed 's/[0-9]//g')
  # Send the notification
  notify-send.py -i "$icon" --replaces-process Brightness -u normal Brightness "|$bar|\n$brightnesspad%"
}

case $1 in
  up)
    # increase the backlight by 5%
    xbacklight -inc 5
    send_notification
    ;;
  down)
    # decrease the backlight by 5%
    xbacklight -dec 5
    send_notification
    ;;
esac
