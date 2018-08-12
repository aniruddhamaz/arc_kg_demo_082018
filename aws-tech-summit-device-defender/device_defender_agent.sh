#!/usr/bin/env bash
bold=$(tput bold)
normal=$(tput sgr0)
red=$(tput setaf 1)
green=$(tput setaf 2)
white=$(tput setaf 7)
clear
echo -n ${bold}
echo     "-------------------------------------------------------"
echo     "| AWS APJC Tech Summit 2018 - Chip to Cloud Security  |"
echo     "-------------------------------------------------------"
echo -n  "${bold}"
python measurement_agent.py -e a1z430h8vzv5nb.iot.us-east-1.amazonaws.com -r /home/pi/deviceSDK/root.cert -c /home/pi/deviceSDK/9b5d9e9e54-certificate.pem.crt -k /home/pi/deviceSDK/9b5d9e9e54-private.pem.key -id MyRaspberryPi -f json -i 60
