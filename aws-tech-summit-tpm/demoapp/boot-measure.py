import hashlib
import binascii
import base64
import subprocess
import os
import tempfile

from tpmutils import *

# --- Measure the TPM for the BIOS, MBR and pre-kernel code ---	

def measureAndUpdateBIOS(files):
	#Take measurements and compute a possible PCR value assuming the inital PCR value is 0000000000000000000000000000000000000000

	tpmPath = TPM_TSS_UTILS_DIR 

	with open(DATA_DIR + "/bios_measurements", 'w') as biosfile:
		pcrNum = 0
		for f in files:
			
			fileDigest = getFileDigest(f)
			fileDigestStr = binascii.hexlify(fileDigest).decode("ascii")
						
			tmpFile = tempfile.NamedTemporaryFile(mode="w+b", prefix="tpm-", suffix="-mdigest", delete=False)
			tmpFile.write(fileDigest)
			tmpFile.close()
			
			cmd = "./pcrextend -ha {0} -halg sha1 -if {1}".format(pcrNum, tmpFile.name)
			
			proc = subprocess.Popen(cmd, -1, shell=True, cwd=tpmPath, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) 
			for line in proc.stdout.readlines():
				print(line)
			proc.wait()
						
			currentPCRStr = getPCR(pcrNum)
			
			out = "{0:02d} {1:20s} ima-ng sha1:{2:20s} {3}\n".format(pcrNum, currentPCRStr, fileDigestStr, f)
			biosfile.write(out)	
			pcrNum = pcrNum + 1	



# --- Measure the TPM for the Kernel, OS & Apps ---	
def measureAndUpdatePCR(files, pcrNum):

	#Take measurements and compute a possible PCR value assuming the inital PCR value is 0000000000000000000000000000000000000000

	tpmPath = TPM_TSS_UTILS_DIR 

	with open(DATA_DIR + "/boot_measurements", 'w') as imafile:
	
		for f in files:
			
			fileDigest = getFileDigest(f)
			fileDigestStr = binascii.hexlify(fileDigest).decode("ascii")
						
			tmpFile = tempfile.NamedTemporaryFile(mode="w+b", prefix="tpm-", suffix="-mdigest", delete=False)
			tmpFile.write(fileDigest)
			tmpFile.close()
			
			cmd = "./pcrextend -ha {0} -halg sha1 -if {1}".format(pcrNum, tmpFile.name)
			
			proc = subprocess.Popen(cmd, -1, shell=True, cwd=tpmPath, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) 
			for line in proc.stdout.readlines():
				print(line)
			proc.wait()
						
			currentPCRStr = getPCR(pcrNum)
			
			out = "{0:02d} {1:20s} ima-ng sha1:{2:20s} {3}\n".format(pcrNum, currentPCRStr, fileDigestStr, f)
			imafile.write(out)		
		
		
# ----------------------------------------------------------------------
# Perform the measurements		
measureAndUpdateBIOS (PRE_OS_LOAD_FILES_PI)		
measureAndUpdatePCR(MEASUREMENT_FILES, BOOT_PCR)


