#!/bin/sh
cd /home/pi/arrosage &&
python3 main.py &
python3 automation.py &
python3 mqtt_publish.py &
python3 mqtt_subscribe.py &

