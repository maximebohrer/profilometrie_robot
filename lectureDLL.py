import ctypes as ct
import os
import time
import copy

# codes d'erreur
LJV7IF_RC_OK = 0x0000						# Normal termination
LJV7IF_RC_ERR_OPEN = 0x1000					# Failed to open the communication path
LJV7IF_RC_ERR_NOT_OPEN = 0x1001				# The communication path was not established.
LJV7IF_RC_ERR_SEND = 0x1002					# Failed to send the command.
LJV7IF_RC_ERR_RECEIVE = 0x1003				# Failed to receive a response.
LJV7IF_RC_ERR_TIMEOUT = 0x1004				# A timeout occurred while waiting for the response.
LJV7IF_RC_ERR_NOMEMORY = 0x1005				# Failed to allocate memory.
LJV7IF_RC_ERR_PARAMETER = 0x1006			# An invalid parameter was passed.
LJV7IF_RC_ERR_RECV_FMT = 0x1007				# The received response data was invalid
LJV7IF_RC_ERR_HISPEED_NO_DEVICE = 0x1009	# High-speed communication initialization could not be performed.
LJV7IF_RC_ERR_HISPEED_OPEN_YET = 0x100A		# High-speed communication was initialized.
LJV7IF_RC_ERR_HISPEED_RECV_YET = 0x100B		# Error already occurred during high-speed communication (for high-speed communication)
LJV7IF_RC_ERR_BUFFER_SHORT = 0x100C			# The buffer size passed as an argument is insufficient. 

WORD = ct.c_ushort # 2 bytes | 16 bits
DWORD = ct.c_ulong # 8 bytes | 32 bits

dbTravelLength = 0
dbYStep = 0

iMAX_MEASURE_DATA = 16                        # -> number of output (digital)
iMAX_DATA = 800                               # -> base length of a profile
dbSENSOR_RESOLUTION_IN_mm = 1e-5           # -> sensor resolution in mm along Z
ProInf = LJV7IF_PROFILE_INFO()         # -> information about the curent profile
dbSENSOR_RESOLUTION_IN_mm_X = 1e-5         # -> sensor resolution in mm along X
dbXResolution = dbSENSOR_RESOLUTION_IN_mm_X   # ->default resolution along X
fProfileFileName = "PROFILE_DATA.TXT"      # -> name of the profile file name
f3DProfileFileName = "PROFILE_DATA_3D.TXT" # -> name of the 3D profile file (RAW)
iHEADER_SIZE = 24                             # -> data header structure's length ( 6 x sizeof(DWORD))
iFOOTER_SIZE = 4

mydll = ct.cdll.LoadLibrary(os.path.join(os.getcwd(), "LJV7_IF.dll")) #"C:/Users/profilometre/Desktop/profilometrie_robot/LJV7_IF.dll")

class LJV7IF_ETHERNET_CONFIG(ct.Structure):
	_fields_ = [
		("abyIpAddress", ct.c_byte * 4),
		("wPortNo", ct.c_ushort),
		("reserve", ct.c_byte * 2)
	]

class LJV7IF_HIGH_SPEED_PRE_START_REQ(ct.Structure):
	_fields_ = [
		("bySendPos", ct.c_byte),
		("reserve", ct.c_byte * 3)
	]

class LJV7IF_PROFILE_INFO(ct.Structure):
	_fields_ = [
		("byProfileCnt", ct.c_byte),
		("byEnvelope", ct.c_byte),
		("reserve", ct.c_byte * 2),
		("wProfDataCnt", ct.c_ushort),
		("reserve2", ct.c_byte * 2),
		("IXStart", ct.c_long),
		("IXPitch", ct.c_long)
	]

class LJV7IF_MEASURE_DATA(ct.Structure):
	_fields_ = [
		("byDataInfo", ct.c_byte),
		("byJudge", ct.c_byte),
		("reserve", ct.c_byte * 2),
		("fvalue", ct.c_float)
	]

class LJV7IF_GET_BATCH_PROFILE_ADVANCE_REQ(ct.Structure):
	_fields_ = [
		("byPosMode", ct.c_byte),
		("reserve", ct.c_byte * 3),
		("dwGetBatchNo", ct.c_ulong),
		("dwGetProfNo", ct.c_ulong),
		("byGetProfCnt", ct.c_byte),
		("reserve", ct.c_byte * 3)
	]

class LJV7IF_GET_BATCH_PROFILE_ADVANCE_RSP(ct.Structure):
	_fields_ = [
		("dwGetBatchNo", ct.c_ulong),
		("dwGetBatchProfCnt", ct.c_ulong),
		("dwGetBatchTopProfNo", ct.c_ulong),
		("byGetProfCnt", ct.c_byte),
		("reserve", ct.c_byte * 3)
	]

class LJV7IF_GET_PROFILE_REQ(ct.Structure):
	_fields_ = [
		("byTargetBank", ct.c_byte),
		("byPosMode", ct.c_byte),
		("reserve", ct.c_byte * 2),
		("dwGetProfNo", ct.c_ulong),
		("byGetProfCnt", ct.c_byte),
		("byErase", ct.c_byte),
		("reserve", ct.c_byte * 2)
	]

class LJV7IF_PROFILE_HEADER(ct.Structure):
	_fields_ = [
		("reserve", ct.c_ulong),
		("dwTriggerCnt", ct.c_ulong),
		("dwEncoderCnt", ct.c_ulong),
		("reserve2", ct.c_ulong * 3)
	]

def Initialize():
	res = mydll.LJV7IF_Initialize()
	print(f"Initialisation du DLL : {hex(res)}")
	return res

def GetVersion():
	res = mydll.LJV7IF_GetVersion()
	print(f"Version du DLL : {hex(res)}")
	return res

def EthernetOpen(deviceID, ipAddress, port):
	Kconnection = LJV7IF_ETHERNET_CONFIG()
	Kconnection.abyIpAddress[0], Kconnection.abyIpAddress[1], Kconnection.abyIpAddress[2], Kconnection.abyIpAddress[3] = map(lambda x: int(x), ipAddress.split(".", 4))
	Kconnection.wPortNo = port
	res = mydll.LJV7IF_EthernetOpen(deviceID, ct.byref(Kconnection))
	print(f"Connexion à l'adresse IP : {ipAddress}, sur le port {Kconnection.wPortNo} : {hex(res)}")
	return res

def GetMeasurementValue(deviceID):
	pMeasureData = (LJV7IF_MEASURE_DATA * 16)()
	res = mydll.LJV7IF_GetMeasurementValue(deviceID, ct.byref(pMeasureData))
	return 0

def GetProfileAdvance(deviceID):
	resolution = 1e-5
	pProfileInfo = LJV7IF_PROFILE_INFO()
	numberOfInt = 800 + 6 + 1
	dwDataSize = numberOfInt * ct.sizeof(ct.c_ulong)
	pdwProfileData = (ct.c_ulong * numberOfInt)()
	pMeasureData = (LJV7IF_MEASURE_DATA * 16)()

	res = mydll.LJV7IF_GetProfileAdvance(deviceID, ct.byref(pProfileInfo), pdwProfileData, dwDataSize, ct.byref(pMeasureData)) #ct.cast(pMeasureData, ct.POINTER(LJV7IF_MEASURE_DATA))
	print(f"Getting profile advance : {hex(res)}")
	return [(pdwProfileData[i] * resolution) for i in range(6, numberOfInt - 1)]
	#return [(pdwProfileData[i] * resolution) if (pdwProfileData[i] * resolution) < 100 else 0 for i in range(6, numberOfInt - 1)]
	#return [ct.cast(pdwProfileData, ct.POINTER(ct.c_double))[i] * resolution for i in range(6, numberOfInt - 1)]

def GetBatchProfileAdvance(deviceID, dwDataSize):
	pReq = LJV7IF_GET_BATCH_PROFILE_ADVANCE_REQ()
	pRsp = LJV7IF_GET_BATCH_PROFILE_ADVANCE_RSP()
	pProfileInfo = LJV7IF_PROFILE_INFO()
	pdwBatchData = ct.c_ulong()
	pBatchMeasureData = LJV7IF_MEASURE_DATA()
	pMeasureData = LJV7IF_MEASURE_DATA()

	res = mydll.LJV7IF_GetBatchProfileAdvance(deviceID, ct.POINTER(pReq), ct.POINTER(pRsp), ct.POINTER(pProfileInfo), ct.POINTER(pdwBatchData), dwDataSize, ct.POINTER(pBatchMeasureData), ct.POINTER(pMeasureData))
	return res

def CommClose(deviceID):
	res = mydll.LJV7IF_CommClose(deviceID)
	print(f"Fin de la connexion avec device {deviceID} : {hex(res)}")
	return res

def Finalize():
	res = mydll.LJV7IF_Finalize()
	print(f"Finalisation du DLL : {hex(res)}")
	return res

'''
def HighSpeedDataEthernetCommunicationInitialize(deviceID, ipAddress, port):
	data = 0
	def mafonctioncallback(pBuffer, dwSize, dwCount, dwNotify, dwUser):
		print(pBuffer)
	prototype = ct.CFUNCTYPE(ct.c_void_p, ct.POINTER(ct.c_byte),
			  ct.c_ulong, ct.c_ulong, ct.c_ulong, ct.c_ulong)
		
	Kconnection = LJV7IF_ETHERNET_CONFIG()
	Kconnection.abyIpAddress[0], Kconnection.abyIpAddress[1], Kconnection.abyIpAddress[2], Kconnection.abyIpAddress[3] = map(lambda x: int(x), ipAddress.split(".", 4))
	Kconnection.wPortNo = port
	res = mydll.LJV7IF_HighSpeedDataEthernetCommunicationInitalize(deviceID, ct.byref(Kconnection), prototype(mafonctioncallback))
	print(f"Initialisation connexion rapide à l'adresse IP : {ipAddress}, sur le port {Kconnection.wPortNo} : {hex(res)}")
	return (res, data)

def GetProfile(deviceID, bySendPos, dwDataSize):
	req = LJV7IF_HIGH_SPEED_PRE_START_REQ()
	req.bySendPos = bySendPos
	res = mydll.LJV7IF_GetProfile(deviceID, req, dwDataSize)
	print("Récupération profile")
	return res

def GetProfileValues(profileData, dbData):
	# Array.Copy(arIntSrcData, (iHEADER_SIZE / sizeof(Int64)), dbValues, 0, iMAX_DATA);
	dbValues = copy.deepcopy(profileData)
	for i in range (iMAX_DATA):
		dbValues[i] = dbSENSOR_RESOLUTION_IN_mm * dbValues[i]
	return iMAX_DATA

def WriteProfileDataToTextFile(dbValues, iSize, sFileName):
	f = open(sFileName, "w")
	
	dbTemp = 0                                                          # ->intermediate value
	dbX = 0                                                             # ->x value for profile's point
	dbStep = 0

	for i in range (iSize):
		dbStep = ProInf.lXPitch
		dbX = (ProInf.lXStart + i * dbStep) * dbXResolution
		dbTemp = dbValues[i] * dbSENSOR_RESOLUTION_IN_mm
		f.write(str(dbX) + "\t" + str(dbTemp))
	f.close()
	
	return 0		

def PreStartHighSpeedDataCommunication(deviceID, bySendPos):
	req = LJV7IF_HIGH_SPEED_PRE_START_REQ()
	req.bySendPos = bySendPos

	pProfileInfo = LJV7IF_PROFILE_INFO()

	res = mydll.LJV7IF_PreStartHighSpeedDataCommunication(deviceID, ct.byref(req), ct.byref(pProfileInfo))
	print(f"Pre start high speed data communication : {hex(res)}")

	return pProfileInfo

def StartHighSpeedDataCommunication(deviceID):
	res = mydll.LJV7IF_StartHighSpeedDataCommunication(deviceID)
	print(f"Starting high speed data communication : {hex(res)}")
	return res

def StopHighSpeedDataCommunication(deviceID):
	res = mydll.LJV7IF_StopHighSpeedDataCommunication(deviceID)
	print(f"Stoping high speed data communication : {hex(res)}")
	return res

def HighSpeedDataCommunicationFinalize(deviceID):
	res = mydll.LJV7IF_HighSpeedDataCommunicationFinalize(deviceID)
	print(f"Finalizing high speed data communication : {hex(res)}")
	return res

def StartMeasure(deviceID):
	res = mydll.LJV7IF_StartMeasure(deviceID)
	print(f"Début de la mesure : {hex(res)}")
	return res

def StopMeasure(deviceID):
	res = mydll.LJV7IF_StopMeasure(deviceID)
	print(f"Fin de la mesure : {hex(res)}")
	return res
'''
#############################################################################################
# Script principal
deviceID = 0
ipAddress = "10.2.34.1"
port = 24691
portHighSpeed = 24692

Initialize()
GetVersion()
EthernetOpen(deviceID, ipAddress, port)
#a = GetProfileAdvance(deviceID, 800)
GetMeasurementValue(deviceID)
a = GetProfileAdvance(deviceID)
print(a)
print("\n".join(map(lambda x: str(x), a)))

input("Fin de la sim ? [ENTER]")
CommClose(deviceID)
Finalize()