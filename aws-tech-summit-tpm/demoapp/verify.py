import hashlib
import binascii
import base64
import subprocess
import os
from time import sleep

from tpmutils import *

tpmPcrValueToCompare = ""
	
def measure(files, pcrNum):

	#Take measurements and compute a possible PCR value assuming the inital PCR value is 0000000000000000000000000000000000000000

	initialPCRValue = base64.b16decode('0000000000000000000000000000000000000000')
	
	lastPCR = initialPCRValue
	
	with open(DATA_DIR + "/runtime_measurements", "w") as runtimefile:
		for f in files:
			sleep (1)
			pcrHash = hashlib.sha1()

			#Update the PCR hash with the initial PCR value
			pcrHash.update(lastPCR)
			
			fileDigest = getFileDigest(f)
			fileDigestStr = binascii.hexlify(fileDigest).decode("ascii")
					
			#Update the PCR hash with this files hash
			pcrHash.update(fileDigest)
			
			lastPCR = pcrHash.digest()
			
			lastPCRStr = binascii.hexlify(lastPCR).decode()
			
			print ("|  " + str(pcrNum) + "    |  " + lastPCRStr + "  |     " + f[f.rfind("/") : ] + " |")	
			
			out = "{0:02d} {1:20s} ima-ng sha1:{2:20s} {3}\n".format(pcrNum, lastPCRStr, fileDigestStr, f)
			runtimefile.write(out)		
			
		
	computedPCRValue = pcrHash.digest()

	return lastPCRStr


# ----------------------------------------------------------------------

# Step 1 : 

print ("")
print ("-----------------------------------------------------------")
print ("Reading PCRs recorded in TPM during boot time")
print ("")
print ("| PCR #  |                  PCR Value                 |")
with open(DATA_DIR + "/runtime_pcr", 'w') as pcrfile:
	for pcr in range(0, 11):
		sleep (1)
		pcrValue = getPCR(pcr)
		print ("|  " + str(pcr) + "     |  " + pcrValue + "  |") 	
		out = "{0:02d} {1:20s}\n".format(pcr, pcrValue)
		if (pcr == 10):
			tpmPcrValueToCompare = pcrValue
		pcrfile.write(out)

# Step 2 : Perform runtime measurements	
print ("----------------------------------------------------------------------")
print ("Performing current measurements of Kernel files & Critical Application")
print ("")
print ("| PCR #  |                  PCR Value                 |     File Name        |")
computedPCR = measure(MEASUREMENT_FILES, BOOT_PCR)
print ("")

if (computedPCR == tpmPcrValueToCompare):
	print ("-----------------------------------------------------------------------------")
	print ("Verification has passed. Current file measurements match TPM recorded values.")
	print ("---------------------------------------------------------------------------------------")
	print ("| "+ computedPCR + " = " + tpmPcrValueToCompare + " |")
	print ("---------------------------------------------------------------------------------------")
else:
	print ("Verification has failed. Current file measurements don't match TPM recorded values")
	print ("----------------------------------------------------------------------------------------")
	print ("| "+ computedPCR + " != " + tpmPcrValueToCompare + " |")
	print ("----------------------------------------------------------------------------------------")
	



