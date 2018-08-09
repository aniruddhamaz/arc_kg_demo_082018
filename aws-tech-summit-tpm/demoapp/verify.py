import hashlib
import binascii
import base64
import subprocess
import os

from tpmutils import *

	
def measure(files, pcrNum):

	#Take measurements and compute a possible PCR value assuming the inital PCR value is 0000000000000000000000000000000000000000

	initialPCRValue = base64.b16decode('0000000000000000000000000000000000000000')
	
	lastPCR = initialPCRValue
	
	with open(DATA_DIR + "/runtime_measurements", "w") as runtimefile:
		for f in files:

			pcrHash = hashlib.sha1()

			#Update the PCR hash with the initial PCR value
			pcrHash.update(lastPCR)
			
			fileDigest = getFileDigest(f)
			fileDigestStr = binascii.hexlify(fileDigest).decode("ascii")
					
			#Update the PCR hash with this files hash
			pcrHash.update(fileDigest)
			
			lastPCR = pcrHash.digest()
			
			lastPCRStr = binascii.hexlify(lastPCR).decode()
			
			out = "{0:02d} {1:20s} ima-ng sha1:{2:20s} {3}\n".format(pcrNum, lastPCRStr, fileDigestStr, f)
			runtimefile.write(out)		
			
		
	computedPCRValue = pcrHash.digest()

	return computedPCRValue


# ----------------------------------------------------------------------

# Step 1 : 

print("Reading current PCRs .....")
with open(DATA_DIR + "/runtime_pcr", 'w') as pcrfile:
	for pcr in range(0, 16):
		pcrValue = getPCR(pcr)
		out = "{0:02d} {1:20s}\n".format(pcr, pcrValue)
		pcrfile.write(out)


# Step 2 : Perform runtime measurements	
print("Performing runtime measurements ....")
computedPCR = measure(MEASUREMENT_FILES, BOOT_PCR)


