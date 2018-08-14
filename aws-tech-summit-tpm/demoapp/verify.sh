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
echo -n  "${bold}${white}"
echo     "Verifying runtime integrity of the device"

python verify.py
