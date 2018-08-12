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
echo     "Detected unauthorized file changes (malware?). Cleaning in progress."
echo -ne '===========                                              (33%)\r'
sleep 2
echo -ne '=========================                                (66%)\r'
sleep 2
echo -ne '========================================                (100%)\r'
echo -ne '\n'

ln -sf /home/pi/arc_kg_demo_082018/aws-tech-summit-tpm/demoapp/app/GoodFile.txt /home/pi/arc_kg_demo_082018/aws-tech-summit-tpm/demoapp/app/app.conf

#echo "Trying out the spinner"
#i=1
#sp="/-\|"
#echo -n ' '
#while (true)
#do
#    printf "\b${sp:i++%${#sp}:1}"
#done

echo -ne "${green}"
echo     "Cleaned Malware. Normal system operations restored."
echo     "-------------------------------------------------------"
echo -ne "${normal}"
