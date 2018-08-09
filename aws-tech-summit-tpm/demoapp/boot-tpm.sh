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


echo "---Starting TPM Server...."

TPM_SERVER_PID=`pgrep -o -x tpm_server`

if [ -n "${TPM_SERVER_PID}" ]; then
	echo "---TPM Server is already running (${TPM_SERVER_PID}) so killing it"
	kill -SIGHUP ${TPM_SERVER_PID}
	sleep 1
fi


cd ${TPM_SW_BASE}/src/
./tpm_server > /dev/null &

sleep 2

echo "---Powering up the TPM...."

cd ${TPM_TSS_BASE}/utils/
./powerup -v
sleep 1
./startup -v


python3 ${DEMOAPP_DIR}/boot-measure.py 



