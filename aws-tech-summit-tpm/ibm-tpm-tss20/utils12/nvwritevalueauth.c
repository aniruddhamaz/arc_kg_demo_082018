/********************************************************************************/
/*										*/
/*			    TPM 1.2 NV_WriteValueAuth				*/
/*			     Written by Ken Goldman				*/
/*		       IBM Thomas J. Watson Research Center			*/
/*	      $Id: nvwritevalueauth.c 1158 2018-04-17 14:41:00Z kgoldman $		*/
/*										*/
/* (c) Copyright IBM Corporation 2018.						*/
/*										*/
/* All rights reserved.								*/
/* 										*/
/* Redistribution and use in source and binary forms, with or without		*/
/* modification, are permitted provided that the following conditions are	*/
/* met:										*/
/* 										*/
/* Redistributions of source code must retain the above copyright notice,	*/
/* this list of conditions and the following disclaimer.			*/
/* 										*/
/* Redistributions in binary form must reproduce the above copyright		*/
/* notice, this list of conditions and the following disclaimer in the		*/
/* documentation and/or other materials provided with the distribution.		*/
/* 										*/
/* Neither the names of the IBM Corporation nor the names of its		*/
/* contributors may be used to endorse or promote products derived from		*/
/* this software without specific prior written permission.			*/
/* 										*/
/* THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS		*/
/* "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT		*/
/* LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR	*/
/* A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT		*/
/* HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,	*/
/* SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT		*/
/* LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,	*/
/* DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY	*/
/* THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT		*/
/* (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE	*/
/* OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.		*/
/********************************************************************************/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#include <tss2/tss.h>
#include <tss2/tssutils.h>
#include <tss2/tssresponsecode.h>
#include <tss2/tsscryptoh.h>
#include <tss2/tpmstructures12.h>
#include <tss2/tssmarshal12.h>
#include <tss2/Unmarshal12_fp.h>

static void printUsage(void);

int verbose = FALSE;

int main(int argc, char * argv[])
{
    TPM_RC 			rc = 0;
    int				i;				/* argc iterator */
    TSS_CONTEXT			*tssContext = NULL;
    NV_WriteValueAuth_In	in;
    TPM12_NV_INDEX		nvIndex = 0xfffffffe;
    const char			*nvPassword = NULL; 
    unsigned int		dataSource = 0;
    const char 			*commandData = NULL;
    const char 			*datafilename = NULL;
    uint16_t 			offset = 0;			/* default 0 */
    size_t 			writeLength;		/* file bytes to write */
    unsigned char 		*writeBuffer = NULL; 	/* file buffer to write */
    TPM_AUTHHANDLE 		sessionHandle0 = TPM_RH_NULL;
    unsigned int		sessionAttributes0 = 0;

    setvbuf(stdout, 0, _IONBF, 0);      /* output may be going through pipe to log file */
    TSS_SetProperty(NULL, TPM_TRACE_LEVEL, "1");

    for (i=1 ; (i<argc) && (rc == 0) ; i++) {
	if (strcmp(argv[i],"-ha") == 0) {
	    i++;
	    if (i < argc) {
		sscanf(argv[i],"%x", &nvIndex);
	    }
	    else {
		printf("Missing parameter for -ha\n");
		printUsage();
	    }
	}
	else if (strcmp(argv[i],"-pwdn") == 0) {
	    i++;
	    if (i < argc) {
		nvPassword = argv[i];
	    }
	    else {
		printf("-pwdn option needs a value\n");
		printUsage();
	    }
	}
	else if (strcmp(argv[i],"-ic") == 0) {
	    i++;
	    if (i < argc) {
		commandData = argv[i];
		dataSource++;
	    }
	    else {
		printf("-ic option needs a value\n");
		printUsage();
	    }
	}
	else if (strcmp(argv[i], "-if")  == 0) {
	    i++;
	    if (i < argc) {
		datafilename = argv[i];
		dataSource++;
	    }
	    else {
		printf("-if option needs a value\n");
		printUsage();
	    }
	}
	else if (strcmp(argv[i],"-off") == 0) {
	    i++;
	    if (i < argc) {
		offset = atoi(argv[i]);
	    }
	    else {
		printf("-off option needs a value\n");
		printUsage();
	    }
	}
	else if (strcmp(argv[i],"-se0") == 0) {
	    i++;
	    if (i < argc) {
		sscanf(argv[i],"%x", &sessionHandle0);
	    }
	    else {
		printf("Missing parameter for -se0\n");
		printUsage();
	    }
	    i++;
	    if (i < argc) {
		sscanf(argv[i],"%x", &sessionAttributes0);
		if (sessionAttributes0 > 0xff) {
		    printf("Out of range session attributes for -se0\n");
		    printUsage();
		}
	    }
	    else {
		printf("Missing parameter for -se0\n");
		printUsage();
	    }
	}
	else if (!strcmp(argv[i], "-h")) {
	    printUsage();
	}
	else if (!strcmp(argv[i], "-v")) {
	    verbose = TRUE;
	    TSS_SetProperty(NULL, TPM_TRACE_LEVEL, "2");
	}
	else {
	    printf("\n%s is not a valid option\n", argv[i]);
	    printUsage();
	}
    }
    if (nvIndex == 0xfffffffe) {
	printf("Missing handle parameter -ha\n");
	printUsage();
    }
    if (dataSource > 1) {
	printf("More than one input data source (-if, -ic)\n");
	printUsage();
    }
    /* if there is no input data source, default to 0 byte write */
    if ((rc == 0) && (dataSource == 0)) {
	in.dataSize = 0;
    }
    /* -if, file data can be written in chunks */
    if ((rc == 0) && (datafilename != NULL)) {
	rc = TSS_File_ReadBinaryFile(&writeBuffer,     /* freed @1 */
				     &writeLength,
				     datafilename);
    }
    if ((rc == 0) && (datafilename != NULL)) {
	if (writeLength > MAX_NV_BUFFER_SIZE) {
	    printf("nvwritevalueauth: size %u greater than %u\n",
		   (unsigned int)writeLength, MAX_NV_BUFFER_SIZE);	
	    rc = TSS_RC_INSUFFICIENT_BUFFER;
	}
	else {
	    in.dataSize = writeLength;
	    memcpy(in.data, writeBuffer, writeLength);
	}
    }
    if ((rc == 0) && (commandData != NULL)) {
	if (strlen(commandData) >  MAX_NV_BUFFER_SIZE) {
	    printf("nvwritevalueauth: size %u greater than %u\n",
		   (unsigned int)strlen(commandData), MAX_NV_BUFFER_SIZE);	
	    rc = TSS_RC_INSUFFICIENT_BUFFER;
	}
	else {
	    in.dataSize = strlen(commandData);
	    memcpy(in.data, commandData, strlen(commandData));
	}
    }
    if (rc == 0) {
       in.nvIndex = nvIndex;
       in.offset = offset;
    }
    /* Start a TSS context */
    if (rc == 0) {
	rc = TSS_Create(&tssContext);
    }
    if (rc == 0) {
	rc = TSS_Execute(tssContext,
			 NULL,
			 (COMMAND_PARAMETERS *)&in,
			 NULL,
			 TPM_ORD_NV_WriteValueAuth,
			 sessionHandle0, nvPassword, sessionAttributes0,
			 TPM_RH_NULL, NULL, 0);
    }
    {
	TPM_RC rc1 = TSS_Delete(tssContext);
	if (rc == 0) {
	    rc = rc1;
	}
    }
    if (rc == 0) {
	if (verbose) printf("nvwritevalueauth: success\n");
    }
    else {
	const char *msg;
	const char *submsg;
	const char *num;
	printf("nvwritevalueauth: failed, rc %08x\n", rc);
	TSS_ResponseCode_toString(&msg, &submsg, &num, rc);
	printf("%s%s%s\n", msg, submsg, num);
	rc = EXIT_FAILURE;
    }
    free(writeBuffer);	/* @1 */
    return rc;
}

static void printUsage(void)
{
    printf("\n");
    printf("nvwritevalueauth\n");
    printf("\n");
    printf("Runs TPM_NV_WriteValueAuth\n");
    printf("\n");
    printf("\t-ha NV index handle\n");
    printf("\t[-pwdn password for NV index (default zeros)]\n");
    printf("\t[-ic data string]\n");
    printf("\t[-if data file]\n");
    printf("\t[-off offset (default 0)]\n");
    printf("\n");
    printf("\t-se0 session handle / attributes\n");
    printf("\t\t01 continue\n");
    exit(1);
}

