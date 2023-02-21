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

dbSENSOR_RESOLUTION_IN_mm_X = 1e-5         # -> sensor resolution in mm along X
dbXResolution = dbSENSOR_RESOLUTION_IN_mm_X   # ->default resolution along X
fProfileFileName = "PROFILE_DATA.TXT"      # -> name of the profile file name
f3DProfileFileName = "PROFILE_DATA_3D.TXT" # -> name of the 3D profile file (RAW)
iHEADER_SIZE = 24                             # -> data header structure's length ( 6 x sizeof(DWORD))
iFOOTER_SIZE = 4

SETTING_BATCH_MEASUREMENT_ON = 1				# --> Because it is cute to do it like this
SETTING_BATCH_MEASUREMENT_OFF = 0
SETTING_TRIGGER_MODE_CONTINUOUS = 0
SETTING_TRIGGER_MODE_EXTERNAL = 1
SETTING_TRIGGER_MODE_ENCODER = 2
SETTING_SAMPLING_FREQUENCY_10_HZ = 0
SETTING_SAMPLING_FREQUENCY_20_HZ = 1
SETTING_SAMPLING_FREQUENCY_50_HZ = 2
SETTING_SAMPLING_FREQUENCY_100_HZ = 3
SETTING_SAMPLING_FREQUENCY_200_HZ = 4
SETTING_SAMPLING_FREQUENCY_500_HZ = 5
SETTING_SAMPLING_FREQUENCY_1000_HZ = 6
SETTING_SAMPLING_FREQUENCY_2000_HZ = 7
SETTING_SAMPLING_FREQUENCY_4000_HZ = 8
SETTING_SAMPLING_FREQUENCY_4130_HZ = 9
SETTING_SAMPLING_FREQUENCY_8000_HZ = 10
SETTING_SAMPLING_FREQUENCY_16000_HZ = 11
SETTING_SAMPLING_FREQUENCY_32000_HZ = 12
SETTING_SAMPLING_FREQUENCY_64000_HZ = 13

DEBUG = False

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

class LJV7IF_TARGET_SETTING(ct.Structure):
	_fields_ = [
		("byType", ct.c_byte),
		("byCategory", ct.c_byte),
		("byItem", ct.c_byte),
		("reserve", ct.c_byte),
		("byTarget1", ct.c_byte),
		("byTarget2", ct.c_byte),
		("byTarget3", ct.c_byte),
		("byTarget4", ct.c_byte)
	]

def Initialize(debug = False):
	global DEBUG
	DEBUG = debug
	res = mydll.LJV7IF_Initialize()
	if DEBUG: print(f"Initialisation du DLL : {hex(res)}")
	return res

def GetVersion():
	res = mydll.LJV7IF_GetVersion()
	if DEBUG: print(f"Version du DLL : {hex(res)}")
	return res

def EthernetOpen(deviceID, ipAddress, port):
	Kconnection = LJV7IF_ETHERNET_CONFIG()
	Kconnection.abyIpAddress[0], Kconnection.abyIpAddress[1], Kconnection.abyIpAddress[2], Kconnection.abyIpAddress[3] = map(lambda x: int(x), ipAddress.split(".", 4))
	Kconnection.wPortNo = port
	res = mydll.LJV7IF_EthernetOpen(deviceID, ct.byref(Kconnection))
	if DEBUG: print(f"Connexion à l'adresse IP : {ipAddress}, sur le port {Kconnection.wPortNo} : {hex(res)}")
	return res

def SetSetting(deviceID, byType, byCategory, byItem, byTarget1, byTarget2, byTarget3, byTarget4, pData, dwDataSize):
	byDepth = 1 # 1 pour running, 2 pour sauvegarder dans ROM
	TargetSetting = LJV7IF_TARGET_SETTING()
	if DEBUG: print(type(byType))
	TargetSetting.byType = ct.c_byte(byType)
	TargetSetting.byCategory = ct.c_byte(byCategory)
	TargetSetting.byItem = ct.c_byte(byItem)
	TargetSetting.byTarget1 = ct.c_byte(byTarget1)
	TargetSetting.byTarget2 = ct.c_byte(byTarget2)
	TargetSetting.byTarget3 = ct.c_byte(byTarget3)
	TargetSetting.byTarget4 = ct.c_byte(byTarget4)
	pdwError = ct.c_ulong()

	mydll.LJV7IF_SetSetting(deviceID, byDepth, TargetSetting, ct.byref(pData), dwDataSize, ct.byref(pdwError))
	if DEBUG: print(f"Mise à jour du setting de type : {byType}")
	return pdwError

def SetSetting_TriggerMode(deviceID, program, mode):
	return SetSetting(deviceID, program + 16, 0, 1, 0, 0, 0, 0, ct.c_byte(mode), 1)

def SetSetting_SamplingFrequency(deviceID, program, freq):
	return SetSetting(deviceID, program + 16, 0, 2, 0, 0, 0, 0, ct.c_byte(freq), 1)

def SetSetting_BatchMeasurement(deviceID, program, state):
	return SetSetting(deviceID, program + 16, 0, 3, 0, 0, 0, 0, ct.c_byte(state), 1)







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
	if DEBUG: print(f"Getting profile advance : {hex(res)}")
	return [(pdwProfileData[i] * resolution) for i in range(6, numberOfInt - 1)]
	#return [(pdwProfileData[i] * resolution) if (pdwProfileData[i] * resolution) < 100 else 0 for i in range(6, numberOfInt - 1)]
	#return [ct.cast(pdwProfileData, ct.POINTER(ct.c_double))[i] * resolution for i in range(6, numberOfInt - 1)]

def Trigger(deviceID):
	res = mydll.LJV7IF_Trigger(deviceID)
	if DEBUG: print(f"Trigger : {hex(res)}")
	return res

def StartMeasure(deviceID):
	res = mydll.LJV7IF_StartMeasure(deviceID)
	if DEBUG: print(f"Début de la mesure : {hex(res)}")
	return res

def GetBatchProfileAdvance(deviceID):
	resolution = 1e-5
	pProfileInfo = LJV7IF_PROFILE_INFO()
	numberOfInt = 800 + 6 + 1

	pReq = LJV7IF_GET_BATCH_PROFILE_ADVANCE_REQ()
	pRsp = LJV7IF_GET_BATCH_PROFILE_ADVANCE_RSP()
	pdwBatchData = (ct.c_ulong * numberOfInt)()
	
	dwDataSize = numberOfInt * ct.sizeof(ct.c_ulong)
	
	pBatchMeasureData = LJV7IF_MEASURE_DATA()
	pMeasureData = LJV7IF_MEASURE_DATA()

	res = mydll.LJV7IF_GetBatchProfileAdvance(deviceID, ct.byref(pReq), ct.byref(pRsp), ct.byref(pProfileInfo), ct.byref(pdwBatchData), dwDataSize, ct.byref(pBatchMeasureData), ct.byref(pMeasureData))
	if DEBUG: print(f"Getting batch profile advance : {hex(res)}")
	return [(pdwBatchData[i] * resolution) for i in range(numberOfInt)]

def StopMeasure(deviceID):
	res = mydll.LJV7IF_StopMeasure(deviceID)
	if DEBUG: print(f"Fin de la mesure : {hex(res)}")
	return res

def CommClose(deviceID):
	res = mydll.LJV7IF_CommClose(deviceID)
	if DEBUG: print(f"Fin de la connexion avec device {deviceID} : {hex(res)}")
	return res

def Finalize():
	res = mydll.LJV7IF_Finalize()
	if DEBUG: print(f"Finalisation du DLL : {hex(res)}")
	return res

if __name__ == "__main__":
	pass





'''
def HighSpeedDataEthernetCommunicationInitialize(deviceID, ipAddress, port):
	data = 0
	def mafonctioncallback(pBuffer, dwSize, dwCount, dwNotify, dwUser):
		if DEBUG: print(pBuffer)
	prototype = ct.CFUNCTYPE(ct.c_void_p, ct.POINTER(ct.c_byte),
			  ct.c_ulong, ct.c_ulong, ct.c_ulong, ct.c_ulong)
		
	Kconnection = LJV7IF_ETHERNET_CONFIG()
	Kconnection.abyIpAddress[0], Kconnection.abyIpAddress[1], Kconnection.abyIpAddress[2], Kconnection.abyIpAddress[3] = map(lambda x: int(x), ipAddress.split(".", 4))
	Kconnection.wPortNo = port
	res = mydll.LJV7IF_HighSpeedDataEthernetCommunicationInitalize(deviceID, ct.byref(Kconnection), prototype(mafonctioncallback))
	if DEBUG: print(f"Initialisation connexion rapide à l'adresse IP : {ipAddress}, sur le port {Kconnection.wPortNo} : {hex(res)}")
	return (res, data)

def GetProfile(deviceID, bySendPos, dwDataSize):
	req = LJV7IF_HIGH_SPEED_PRE_START_REQ()
	req.bySendPos = bySendPos
	res = mydll.LJV7IF_GetProfile(deviceID, req, dwDataSize)
	if DEBUG: print("Récupération profile")
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

	ProInf = LJV7IF_PROFILE_INFO()         # -> information about the curent profile

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
	if DEBUG: print(f"Pre start high speed data communication : {hex(res)}")

	return pProfileInfo

def StartHighSpeedDataCommunication(deviceID):
	res = mydll.LJV7IF_StartHighSpeedDataCommunication(deviceID)
	if DEBUG: print(f"Starting high speed data communication : {hex(res)}")
	return res

def StopHighSpeedDataCommunication(deviceID):
	res = mydll.LJV7IF_StopHighSpeedDataCommunication(deviceID)
	if DEBUG: print(f"Stoping high speed data communication : {hex(res)}")
	return res

def HighSpeedDataCommunicationFinalize(deviceID):
	res = mydll.LJV7IF_HighSpeedDataCommunicationFinalize(deviceID)
	if DEBUG: print(f"Finalizing high speed data communication : {hex(res)}")
	return res
'''