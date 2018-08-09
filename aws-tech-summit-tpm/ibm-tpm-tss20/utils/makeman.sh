#!/bin/bash
#
#	$Id: makeman.sh 1203 2018-05-09 18:13:49Z kgoldman $
#
# script to make man pages

mkdir -p man/man1
help2man -h  --version-string="v1233" -n "Runs TPM2_Activatecredential" /usr/bin/tssactivatecredential > man/man1/tssactivatecredential.1
help2man -h  --version-string="v1233" -n "Runs TPM2_Certify" /usr/bin/tsscertify > man/man1/tsscertify.1
help2man -h  --version-string="v1233" -n "Runs TPM2_CertifyCreation" /usr/bin/tsscertifycreation > man/man1/tsscertifycreation.1
help2man -h  --version-string="v1233" -n "Runs TPM2_ChangeEPS" /usr/bin/tsschangeeps > man/man1/tsschangeeps.1
help2man -h  --version-string="v1233" -n "Runs TPM2_ChangePPS" /usr/bin/tsschangepps > man/man1/tsschangepps.1
help2man -h  --version-string="v1233" -n "Runs TPM2_Clear" /usr/bin/tssclear > man/man1/tssclear.1
help2man -h  --version-string="v1233" -n "Runs TPM2_ClearControl" /usr/bin/tssclearcontrol > man/man1/tssclearcontrol.1
help2man -h  --version-string="v1233" -n "Runs TPM2_ClockRateAdjust" /usr/bin/tssclockrateadjust > man/man1/tssclockrateadjust.1
help2man -h  --version-string="v1233" -n "Runs TPM2_ClockSet" /usr/bin/tssclockset > man/man1/tssclockset.1
help2man -h  --version-string="v1233" -n "Runs TPM2_Commit" /usr/bin/tsscommit > man/man1/tsscommit.1
help2man -h  --version-string="v1233" -n "Runs TPM2_ContextLoad" /usr/bin/tsscontextload > man/man1/tsscontextload.1
help2man -h  --version-string="v1233" -n "Runs TPM2_Contextsave" /usr/bin/tsscontextsave > man/man1/tsscontextsave.1
help2man -h  --version-string="v1233" -n "Runs TPM2_Create" /usr/bin/tsscreate > man/man1/tsscreate.1
help2man -h  --version-string="v1233" -n "Runs createek demo" /usr/bin/tsscreateek > man/man1/tsscreateek.1
help2man -h  --version-string="v1233" -n "Runs createekcert demo" /usr/bin/tsscreateekcert > man/man1/tsscreateekcert.1
help2man -h  --version-string="v1233" -n "Runs TPM2_CreateLoaded" /usr/bin/tsscreateloaded > man/man1/tsscreateloaded.1
help2man -h  --version-string="v1233" -n "Runs TPM2_CreatePrimary" /usr/bin/tsscreateprimary > man/man1/tsscreateprimary.1
help2man -h  --version-string="v1233" -n "Runs TPM2_DictionaryAttackLockReset" /usr/bin/tssdictionaryattacklockreset > man/man1/tssdictionaryattacklockreset.1
help2man -h  --version-string="v1233" -n "Runs TPM2_DictionaryAttackParameters" /usr/bin/tssdictionaryattackparameters > man/man1/tssdictionaryattackparameters.1
help2man -h  --version-string="v1233" -n "Runs TPM2_Duplicate" /usr/bin/tssduplicate > man/man1/tssduplicate.1
help2man -h  --version-string="v1233" -n "Runs TPM2_ECC_Parameters" /usr/bin/tsseccparameters > man/man1/tsseccparameters.1
help2man -h  --version-string="v1233" -n "Runs TPM2_EC_ephemeral" /usr/bin/tssecephemeral > man/man1/tssecephemeral.1
help2man -h  --version-string="v1233" -n "Runs TPM2_EncryptDecrypt" /usr/bin/tssencryptdecrypt > man/man1/tssencryptdecrypt.1
help2man -h  --version-string="v1233" -n "Runs TPM2_EventExtend" /usr/bin/tsseventextend > man/man1/tsseventextend.1
help2man -h  --version-string="v1233" -n "Runs TPM2_EventSequenceComplete" /usr/bin/tsseventsequencecomplete > man/man1/tsseventsequencecomplete.1
help2man -h  --version-string="v1233" -n "Runs TPM2_EvictControl" /usr/bin/tssevictcontrol > man/man1/tssevictcontrol.1
help2man -h  --version-string="v1233" -n "Runs TPM2_FlushContext" /usr/bin/tssflushcontext > man/man1/tssflushcontext.1
help2man -h  --version-string="v1233" -n "Runs TPM2_GetCapability" /usr/bin/tssgetcapability > man/man1/tssgetcapability.1
help2man -h  --version-string="v1233" -n "Runs TPM2_GetCommandAuditDigest" /usr/bin/tssgetcommandauditdigest > man/man1/tssgetcommandauditdigest.1
help2man -h  --version-string="v1233" -n "Runs TPM2_GetRandom" /usr/bin/tssgetrandom > man/man1/tssgetrandom.1
help2man -h  --version-string="v1233" -n "Runs TPM2_GetTestResult" /usr/bin/tssgettestresult > man/man1/tssgettestresult.1
help2man -h  --version-string="v1233" -n "Runs TPM2_GetSessionAuditDigest" /usr/bin/tssgetsessionauditdigest > man/man1/tssgetsessionauditdigest.1
help2man -h  --version-string="v1233" -n "Runs TPM2_GetTime" /usr/bin/tssgettime > man/man1/tssgettime.1
help2man -h  --version-string="v1233" -n "Runs TPM2_Hash" /usr/bin/tsshash > man/man1/tsshash.1
help2man -h  --version-string="v1233" -n "Runs TPM2_HashSequenceStart" /usr/bin/tsshashsequencestart > man/man1/tsshashsequencestart.1
help2man -h  --version-string="v1233" -n "Runs TPM2_HierarchyChangeauth" /usr/bin/tsshierarchychangeauth > man/man1/tsshierarchychangeauth.1
help2man -h  --version-string="v1233" -n "Runs TPM2_HierarchyControl" /usr/bin/tsshierarchycontrol > man/man1/tsshierarchycontrol.1
help2man -h  --version-string="v1233" -n "Runs TPM2_Hmac" /usr/bin/tsshmac > man/man1/tsshmac.1
help2man -h  --version-string="v1233" -n "Runs TPM2_HmacStart" /usr/bin/tsshmacstart > man/man1/tsshmacstart.1
help2man -h  --version-string="v1233" -n "Runs imaextend simulation" /usr/bin/tssimaextend > man/man1/tssimaextend.1
help2man -h  --version-string="v1233" -n "Runs TPM2_Import" /usr/bin/tssimport > man/man1/tssimport.1
help2man -h  --version-string="v1233" -n "Runs TPM2_Import with PEM input" /usr/bin/tssimportpem > man/man1/tssimportpem.1
help2man -h  --version-string="v1233" -n "Runs TPM2_Load" /usr/bin/tssload > man/man1/tssload.1
help2man -h  --version-string="v1233" -n "Runs TPM2_LoadExternal" /usr/bin/tssloadexternal > man/man1/tssloadexternal.1
help2man -h  --version-string="v1233" -n "Runs TPM2_MakeCredential" /usr/bin/tssmakecredential > man/man1/tssmakecredential.1
help2man -h  --version-string="v1233" -n "Runs TPM2_Ntc2GetConfig" /usr/bin/tssntc2getconfig > man/man1/tssntc2getconfig.1
help2man -h  --version-string="v1233" -n "Runs TPM2_Ntc2LockConfig" /usr/bin/tssntc2lockconfig > man/man1/tssntc2lockconfig.1
help2man -h  --version-string="v1233" -n "Runs TPM2_Ntc2Preconfig" /usr/bin/tssntc2preconfig > man/man1/tssntc2preconfig.1
help2man -h  --version-string="v1233" -n "Runs TPM2_NV_Certify" /usr/bin/tssnvcertify > man/man1/tssnvcertify.1
help2man -h  --version-string="v1233" -n "Runs TPM2_NV_ChangeAuth" /usr/bin/tssnvchangeauth > man/man1/tssnvchangeauth.1
help2man -h  --version-string="v1233" -n "Runs TPM2_NV_DefineSpace" /usr/bin/tssnvdefinespace > man/man1/tssnvdefinespace.1
help2man -h  --version-string="v1233" -n "Runs TPM2_NV_Extend" /usr/bin/tssnvextend > man/man1/tssnvextend.1
help2man -h  --version-string="v1233" -n "Runs TPM2_NV_GlobalWriteLock" /usr/bin/tssnvglobalwritelock > man/man1/tssnvglobalwritelock.1
help2man -h  --version-string="v1233" -n "Runs TPM2_NV_Increment" /usr/bin/tssnvincrement > man/man1/tssnvincrement.1
help2man -h  --version-string="v1233" -n "Runs TPM2_NV_Read" /usr/bin/tssnvread > man/man1/tssnvread.1
help2man -h  --version-string="v1233" -n "Runs TPM2_NV_ReadLock" /usr/bin/tssnvreadlock > man/man1/tssnvreadlock.1
help2man -h  --version-string="v1233" -n "Runs TPM2_NV_ReadPublic" /usr/bin/tssnvreadpublic > man/man1/tssnvreadpublic.1
help2man -h  --version-string="v1233" -n "Runs TPM2_NV_SetBits" /usr/bin/tssnvsetbits > man/man1/tssnvsetbits.1
help2man -h  --version-string="v1233" -n "Runs TPM2_NV_UndefineSpace" /usr/bin/tssnvundefinespace > man/man1/tssnvundefinespace.1
help2man -h  --version-string="v1233" -n "Runs TPM2_NV_UndefineSpaceSpecial" /usr/bin/tssnvundefinespacespecial > man/man1/tssnvundefinespacespecial.1
help2man -h  --version-string="v1233" -n "Runs TPM2_NV_Write" /usr/bin/tssnvwrite > man/man1/tssnvwrite.1
help2man -h  --version-string="v1233" -n "Runs TPM2_NV_Writelock" /usr/bin/tssnvwritelock > man/man1/tssnvwritelock.1
help2man -h  --version-string="v1233" -n "Runs TPM2_Objectchangeauth" /usr/bin/tssobjectchangeauth > man/man1/tssobjectchangeauth.1
help2man -h  --version-string="v1233" -n "Runs TPM2_PCR_Allocate" /usr/bin/tsspcrallocate > man/man1/tsspcrallocate.1
help2man -h  --version-string="v1233" -n "Runs TPM2_PCR_Event" /usr/bin/tsspcrevent > man/man1/tsspcrevent.1
help2man -h  --version-string="v1233" -n "Runs TPM2_PCR_Extend" /usr/bin/tsspcrextend > man/man1/tsspcrextend.1
help2man -h  --version-string="v1233" -n "Runs TPM2_PCR_Read" /usr/bin/tsspcrread > man/man1/tsspcrread.1
help2man -h  --version-string="v1233" -n "Runs TPM2_PCR_Reset" /usr/bin/tsspcrreset > man/man1/tsspcrreset.1
help2man -h  --version-string="v1233" -n "Runs TPM2_PolicyAuthorize" /usr/bin/tsspolicyauthorize > man/man1/tsspolicyauthorize.1
help2man -h  --version-string="v1233" -n "Runs TPM2_PolicyAuthorizeNV" /usr/bin/tsspolicyauthorizenv > man/man1/tsspolicyauthorizenv.1
help2man -h  --version-string="v1233" -n "Runs TPM2_PolicyAuthValue" /usr/bin/tsspolicyauthvalue > man/man1/tsspolicyauthvalue.1
help2man -h  --version-string="v1233" -n "Runs TPM2_PolicyCommandCode" /usr/bin/tsspolicycommandcode > man/man1/tsspolicycommandcode.1
help2man -h  --version-string="v1233" -n "Runs TPM2_PolicyCounterTimer" /usr/bin/tsspolicycountertimer > man/man1/tsspolicycountertimer.1
help2man -h  --version-string="v1233" -n "Runs TPM2_PolicyCpHash" /usr/bin/tsspolicycphash > man/man1/tsspolicycphash.1
help2man -h  --version-string="v1233" -n "Runs TPM2_PolicyDuplicationSelect" /usr/bin/tsspolicyduplicationselect > man/man1/tsspolicyduplicationselect.1
help2man -h  --version-string="v1233" -n "Runs TPM2_PolicyGetDigest" /usr/bin/tsspolicygetdigest > man/man1/tsspolicygetdigest.1
help2man -h  --version-string="v1233" -n "Runs policymaker utility" /usr/bin/tsspolicymaker > man/man1/tsspolicymaker.1
help2man -h  --version-string="v1233" -n "Runs policymakerpcr utility" /usr/bin/tsspolicymakerpcr > man/man1/tsspolicymakerpcr.1
help2man -h  --version-string="v1233" -n "Runs TPM2_PolicyNv" /usr/bin/tsspolicynv > man/man1/tsspolicynv.1
help2man -h  --version-string="v1233" -n "Runs TPM2_PolicyNvWritten" /usr/bin/tsspolicynvwritten > man/man1/tsspolicynvwritten.1
help2man -h  --version-string="v1233" -n "Runs TPM2_PolicyOR" /usr/bin/tsspolicyor > man/man1/tsspolicyor.1
help2man -h  --version-string="v1233" -n "Runs TPM2_PolicyPassword" /usr/bin/tsspolicypassword > man/man1/tsspolicypassword.1
help2man -h  --version-string="v1233" -n "Runs TPM2_PolicyPCR" /usr/bin/tsspolicypcr > man/man1/tsspolicypcr.1
help2man -h  --version-string="v1233" -n "Runs TPM2_PolicyRestart" /usr/bin/tsspolicyrestart > man/man1/tsspolicyrestart.1
help2man -h  --version-string="v1233" -n "Runs TPM2_PolicySecret" /usr/bin/tsspolicysecret > man/man1/tsspolicysecret.1
help2man -h  --version-string="v1233" -n "Runs TPM2_PolicySigned" /usr/bin/tsspolicysigned > man/man1/tsspolicysigned.1
help2man -h  --version-string="v1233" -n "Runs TPM2_PolicyTemplate" /usr/bin/tsspolicytemplate > man/man1/tsspolicytemplate.1
help2man -h  --version-string="v1233" -n "Runs TPM2_PolicyTicket" /usr/bin/tsspolicyticket > man/man1/tsspolicyticket.1
help2man -h  --version-string="v1233" -n "Runs powerup simulation" /usr/bin/tsspowerup > man/man1/tsspowerup.1
help2man -h  --version-string="v1233" -n "Runs TPM2_Quote" /usr/bin/tssquote > man/man1/tssquote.1
help2man -h  --version-string="v1233" -n "Runs TPM2_ReadClock" /usr/bin/tssreadclock > man/man1/tssreadclock.1
help2man -h  --version-string="v1233" -n "Runs TPM2_ReadPublic" /usr/bin/tssreadpublic > man/man1/tssreadpublic.1
help2man -h  --version-string="v1233" -n "Runs returncode parser" /usr/bin/tssreturncode > man/man1/tssreturncode.1
help2man -h  --version-string="v1233" -n "Runs TPM2_Rewrap" /usr/bin/tssrewrap > man/man1/tssrewrap.1
help2man -h  --version-string="v1233" -n "Runs TPM2_RsaDecrypt" /usr/bin/tssrsadecrypt > man/man1/tssrsadecrypt.1
help2man -h  --version-string="v1233" -n "Runs TPM2_RsaEncrypt" /usr/bin/tssrsaencrypt > man/man1/tssrsaencrypt.1
help2man -h  --version-string="v1233" -n "Runs TPM2_SequenceComplete" /usr/bin/tsssequencecomplete > man/man1/tsssequencecomplete.1
help2man -h  --version-string="v1233" -n "Runs TPM2_SequenceUpdate" /usr/bin/tsssequenceupdate > man/man1/tsssequenceupdate.1
help2man -h  --version-string="v1233" -n "Runs TPM2_SetPrimarypolicy" /usr/bin/tsssetprimarypolicy > man/man1/tsssetprimarypolicy.1
help2man -h  --version-string="v1233" -n "Runs TPM2_Shutdown" /usr/bin/tssshutdown > man/man1/tssshutdown.1
help2man -h  --version-string="v1233" -n "Runs TPM2_Sign" /usr/bin/tsssign > man/man1/tsssign.1
help2man -h  --version-string="v1233" -n "Runs TPM2_Signapp" /usr/bin/tsssignapp > man/man1/tsssignapp.1
help2man -h  --version-string="v1233" -n "Runs TPM2_StartAuthSession" /usr/bin/tssstartauthsession > man/man1/tssstartauthsession.1
help2man -h  --version-string="v1233" -n "Runs TPM2_Startup" /usr/bin/tssstartup > man/man1/tssstartup.1
help2man -h  --version-string="v1233" -n "Runs TPM2_StirRandom" /usr/bin/tssstirrandom > man/man1/tssstirrandom.1
help2man -h  --version-string="v1233" -n "Runs timepacket profiler" /usr/bin/tsstimepacket > man/man1/tsstimepacket.1
help2man -h  --version-string="v1233" -n "Runs tpm2pem demo" /usr/bin/tsstpm2pem > man/man1/tsstpm2pem.1
help2man -h  --version-string="v1233" -n "Runs tpmpublic2eccpoint demo" /usr/bin/tsstpmpublic2eccpoint > man/man1/tsstpmpublic2eccpoint.1
help2man -h  --version-string="v1233" -n "Runs TPM2_Unseal" /usr/bin/tssunseal > man/man1/tssunseal.1
help2man -h  --version-string="v1233" -n "Runs TPM2_VerifySignature" /usr/bin/tssverifysignature > man/man1/tssverifysignature.1
help2man -h  --version-string="v1233" -n "Runs writeapp demo" /usr/bin/tsswriteapp > man/man1/tsswriteapp.1
help2man -h  --version-string="v1233" -n "Runs TPM2_ZGen_2Phase" /usr/bin/tsszgen2phase > man/man1/tsszgen2phase.1
