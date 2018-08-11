
import hashlib
import subprocess


BUFF_SIZE = 65536

TPM_DIR           = "/home/pi/arc_kg_demo_082018/aws-tech-summit-tpm"
TPM_TSS_BASE_DIR  = TPM_DIR + "/ibm-tpm-tss20"
TPM_TSS_UTILS_DIR = TPM_TSS_BASE_DIR + "/utils"
DEMOAPP_DIR		  = TPM_DIR + "/demoapp"
DATA_DIR          = DEMOAPP_DIR + "/data"

BOOT_PCR		  = 10

MEASUREMENT_FILES_VM = [
	"/initrd.img", 
	"/sbin/init", 
	"/lib/ld-linux.so.2", 
	"/lib/i386-linux-gnu/libx86.so.1", 
	"/lib/i386-linux-gnu/libnss_compat.so.2"
	]

MEASUREMENT_FILES_PI = [
	"/sbin/init",
	"/lib/ld-linux.so.3",
	"/lib/ld-linux-armhf.so.3",
	"/lib/libnih-dbus.so.1",
	"/lib/systemd/systemd",
	"/lib/libnih.so.1",
	"/home/pi/arc_kg_demo_082018/aws-tech-summit-tpm/demoapp/app/app.conf"
]

MEASUREMENT_FILES = MEASUREMENT_FILES_PI

PRE_OS_LOAD_FILES_PI = [
	"/home/pi/arc_kg_demo_082018/aws-tech-summit-tpm/demoapp/boot/bios",
	"/home/pi/arc_kg_demo_082018/aws-tech-summit-tpm/demoapp/boot/bios.conf",
	"/home/pi/arc_kg_demo_082018/aws-tech-summit-tpm/demoapp/boot/optionROM",
	"/home/pi/arc_kg_demo_082018/aws-tech-summit-tpm/demoapp/boot/optionROM.conf",
	"/home/pi/arc_kg_demo_082018/aws-tech-summit-tpm/demoapp/boot/mbr",
	"/home/pi/arc_kg_demo_082018/aws-tech-summit-tpm/demoapp/boot/mbr.conf",
	"/home/pi/arc_kg_demo_082018/aws-tech-summit-tpm/demoapp/boot/libpowerup.so.1",
	"/home/pi/arc_kg_demo_082018/aws-tech-summit-tpm/demoapp/boot/libpowerup.so.2",
	"/home/pi/arc_kg_demo_082018/aws-tech-summit-tpm/demoapp/boot/libexecdsk.so",
	"/home/pi/arc_kg_demo_082018/aws-tech-summit-tpm/demoapp/boot/libsyscore.so"
]

# ----------------------------------------------------------------------
# Gets the files SHA-1 digest
# ----------------------------------------------------------------------
def getFileDigest(infile):
	
	sha1File = hashlib.sha1()
	
	with open(infile, 'rb') as f1:
		while True:
			data = f1.read(BUFF_SIZE)
			if not data:
				break
			sha1File.update(data)
		
	return sha1File.digest()
	

# ----------------------------------------------------------------------
# Reads specified PCR value from the TPM
# ----------------------------------------------------------------------
def getPCR(pcrNum):
	
	tpmPath = TPM_TSS_UTILS_DIR		
		
	cmd = "./pcrread -ha {0} -halg sha1 -ns".format(pcrNum)
	
	proc = subprocess.Popen(cmd, -1, shell=True, cwd=tpmPath, stdout=subprocess.PIPE, stderr=subprocess.PIPE) 
	currentPCR = proc.stdout.readline()		
	proc.wait()		
	
	currentPCRStr = currentPCR.decode()				# Convert bytes to string
	currentPCRStr = currentPCRStr.rstrip()			# Chomp
	
	return currentPCRStr


