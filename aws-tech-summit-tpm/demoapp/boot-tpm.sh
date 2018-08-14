#!/usr/bin/env bash

TPM_BASE=/home/pi/arc_kg_demo_082018/aws-tech-summit-tpm

TPM_SW_BASE=$TPM_BASE/ibm-sw-tpm
TPM_TSS_BASE=$TPM_BASE/ibm-tpm-tss20
DEMOAPP_DIR=$TPM_BASE/demoapp
PCR_OS=8
PCR_ALGO='sha1'

export TPM_BASE
export TPM_SW_BASE
export TPM_TSS_BASE
export PCR_OS
export PCR_ALGO

pcrextendWith() {

test=`sha1sum -b $1`
echo ${test}

./pcrextend -ha ${PCR_OS} -halg ${PCR_ALGO} -ic '`sha1sum -b $1`'

./pcrread -ha ${PCR_OS} -halg ${PCR_ALGO} -ns 
}

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

echo     "Starting TPM Simulation Server...."

TPM_SERVER_PID=`pgrep -o -x tpm_server`

if [ -n "${TPM_SERVER_PID}" ]; then
	echo "TPM Simulation Server is already running (${TPM_SERVER_PID}) so killing it"
	kill -SIGHUP ${TPM_SERVER_PID}
	sleep 1
fi


cd ${TPM_SW_BASE}/src/
./tpm_server > /dev/null &

sleep 2

echo -ne 'Powering up the TPM  ===========                         (33%)\r'
sleep 2
echo -ne 'Powering up the TPM  =========================           (66%)\r'
sleep 2
cd ${TPM_TSS_BASE}/utils/
./powerup
sleep 1
./startup

echo -ne 'Powering up the TPM  ====================================(100%)\r'
echo -ne '\n'
echo     'TPM Simulator started and ready for commands'

python3 ${DEMOAPP_DIR}/boot-measure.py 



