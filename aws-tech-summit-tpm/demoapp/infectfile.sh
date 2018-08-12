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
echo -n  "${bold}${red}"
echo     "Infecting a file (for demo purpose only)!"
echo -ne '===========                                              (33%)\r'
sleep 2
echo -ne '=========================                                (66%)\r'
sleep 2
echo -ne '========================================                (100%)\r'
echo -ne '\n'
echo     "File successfully infected. Now how to verify ? ? ?   "
ln -sf /home/pi/arc_kg_demo_082018/aws-tech-summit-tpm/demoapp/app/BadFile.txt /home/pi/arc_kg_demo_082018/aws-tech-summit-tpm/demoapp/app/app.conf
