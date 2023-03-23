import ctypes as ct
import os

LJV7IF_RC_OK = 0x0000						 # Normal termination
LJV7IF_RC_ERR_OPEN = 0x1000					 # Failed to open the communication path
LJV7IF_RC_ERR_NOT_OPEN = 0x1001				 # The communication path was not established.
LJV7IF_RC_ERR_SEND = 0x1002					 # Failed to send the command.
LJV7IF_RC_ERR_RECEIVE = 0x1003				 # Failed to receive a response.
LJV7IF_RC_ERR_TIMEOUT = 0x1004				 # A timeout occurred while waiting for the response.
LJV7IF_RC_ERR_NOMEMORY = 0x1005				 # Failed to allocate memory.
LJV7IF_RC_ERR_PARAMETER = 0x1006			 # An invalid parameter was passed.
LJV7IF_RC_ERR_RECV_FMT = 0x1007				 # The received response data was invalid
LJV7IF_RC_ERR_HISPEED_NO_DEVICE = 0x1009	 # High-speed communication initialization could not be performed.
LJV7IF_RC_ERR_HISPEED_OPEN_YET = 0x100A		 # High-speed communication was initialized.
LJV7IF_RC_ERR_HISPEED_RECV_YET = 0x100B		 # Error already occurred during high-speed communication (for high-speed communication)
LJV7IF_RC_ERR_BUFFER_SHORT = 0x100C			 # The buffer size passed as an argument is insufficient.

LJV7IF_SETTING_DEPTH_WRITE = 0x00            # Write settings area
LJV7IF_SETTING_DEPTH_RUNNING = 0x01          # Running settings area
LJV7IF_SETTING_DEPTH_SAVE = 0x02             # Save area

LJV7IF_INIT_SETTING_TARGET_PRG0 = 0x00       # Program 0
LJV7IF_INIT_SETTING_TARGET_PRG1 = 0x01       # Program 1
LJV7IF_INIT_SETTING_TARGET_PRG2 = 0x02       # Program 2
LJV7IF_INIT_SETTING_TARGET_PRG3 = 0x03       # Program 3
LJV7IF_INIT_SETTING_TARGET_PRG4 = 0x04       # Program 4
LJV7IF_INIT_SETTING_TARGET_PRG5 = 0x05       # Program 5
LJV7IF_INIT_SETTING_TARGET_PRG6 = 0x06       # Program 6
LJV7IF_INIT_SETTING_TARGET_PRG7 = 0x07       # Program 7
LJV7IF_INIT_SETTING_TARGET_PRG8 = 0x08       # Program 8
LJV7IF_INIT_SETTING_TARGET_PRG9 = 0x09       # Program 9
LJV7IF_INIT_SETTING_TARGET_PRG10 = 0x0A      # Program 10
LJV7IF_INIT_SETTING_TARGET_PRG11 = 0x0B      # Program 11
LJV7IF_INIT_SETTING_TARGET_PRG12 = 0x0C      # Program 12
LJV7IF_INIT_SETTING_TARGET_PRG13 = 0x0D      # Program 13
LJV7IF_INIT_SETTING_TARGET_PRG14 = 0x0E      # Program 14
LJV7IF_INIT_SETTING_TARGET_PRG15 = 0x0F      # Program 15

LJV7IF_MEASURE_DATA_INFO_VALID = 0x00        # Normal measurement data
LJV7IF_MEASURE_DATA_INFO_ALARM = 0x01        # Measurement alarm data
LJV7IF_MEASURE_DATA_INFO_WAIT = 0x02         # Judgment wait data

LJV7IF_JUDGE_RESULT_HI = 0x01                # HI
LJV7IF_JUDGE_RESULT_GO = 0x02                # GO
LJV7IF_JUDGE_RESULT_LO = 0x04                # LO

LJV7IF_PROFILE_BANK_ACTIVE = 0x00            # Active surface
LJV7IF_PROFILE_BANK_INACTIVE = 0x01          # Inactive surface

LJV7IF_PROFILE_POS_CURRENT = 0x00            # From current
LJV7IF_PROFILE_POS_OLDEST = 0x01             # From oldest
LJV7IF_PROFILE_POS_SPEC = 0x02               # Specify position

LJV7IF_BATCH_POS_CURRENT = 0x00              # From current
LJV7IF_BATCH_POS_SPEC = 0x02                 # Specify position
LJV7IF_BATCH_POS_COMMITED = 0x03             # From current after batch commitment
LJV7IF_BATCH_POS_CURRENT_ONLY = 0x04         # Current only

SETTING_BATCH_MEASUREMENT_ON = 1 
SETTING_BATCH_MEASUREMENT_OFF = 0 
SETTING_TRIGGER_MODE_CONTINUOUS = 0          # In batch mode, the profiles are captured automatically at fixed intervals
SETTING_TRIGGER_MODE_EXTERNAL = 1            # In batch mode, the profiles are captured manually using a trigger signal (Trigger function)
SETTING_TRIGGER_MODE_ENCODER = 2             # In batch mode, if an encoder is connected, the profiles are captured automatically each time the encoder value changes
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

WORD = ct.c_ushort # 2 bytes | 16 bits
DWORD = ct.c_ulong # 8 bytes | 32 bits

RESOLUTION = 1e-5

DEBUG = False

dll = ct.cdll.LoadLibrary(os.path.join(os.getcwd(), "LJV7_IF.dll")) #"C:/Users/profilometre/Desktop/profilometrie_robot/LJV7_IF.dll")

class LJV7IF_ETHERNET_CONFIG(ct.Structure):
	_fields_ = [
		("abyIpAddress", ct.c_ubyte * 4),
		("wPortNo", ct.c_ushort),
		("reserve", ct.c_ubyte * 2)
	]

class LJV7IF_HIGH_SPEED_PRE_START_REQ(ct.Structure):
	_fields_ = [
		("bySendPos", ct.c_ubyte),
		("reserve", ct.c_ubyte * 3)
	]

class LJV7IF_PROFILE_INFO(ct.Structure):
	_fields_ = [
		("byProfileCnt", ct.c_ubyte),        # Wheter dicates the amount of profile data stored. (When 2 head/combine (wide) is off, 2 profile data units is stored, otherwise 1 profile data unit is stored.)
		("byEnvelope", ct.c_ubyte),          # Whether profile compression (time axis) is on. 0: off, 1: on.
		("reserve", ct.c_ubyte * 2),
		("wProfDataCnt", ct.c_ushort),      # Profile data count (initial setting: 800).
		("reserve2", ct.c_ubyte * 2),
		("IXStart", ct.c_long),             # 1st point X coordinate.
		("IXPitch", ct.c_long)              # Profile data X direction interval. IXStart and IXPitch are stored in 0.01 μm units.
	]

class LJV7IF_MEASURE_DATA(ct.Structure):
	_fields_ = [
		("byDataInfo", ct.c_ubyte),           # This variable indicates whether or not the measurement value (fValue) is valid, and if it is not a valid value, what kind of data it is. See LJV7IF_MEASURE_DATA_INFO.
		("byJudge", ct.c_ubyte),              # Tolerance judgment result. See LJV7IF_JUDGE_RESULT.
		("reserve", ct.c_ubyte * 2),  
		("fvalue", ct.c_float)               # Measurement value. The unit used for measurement values is the minimum display unit set for Target OUT in program settings. When the minimum display unit is 1 mm to 0.001 mm, the measurement value unit is [mm]. When 1 um to 0.1 um, the measurement value unit is [um]. The unit for sectional areas is mm^2, and the unit for angles is deg. When not a valid value, a large negative value is stored (-10^10).
	]

class LJV7IF_GET_BATCH_PROFILE_ADVANCE_REQ(ct.Structure):
	_fields_ = [
		("byPosMode", ct.c_ubyte),            # Specifies the get profile position specification method. See LJV7IF_BATCH_POS.
		("reserve", ct.c_ubyte * 3),
		("dwGetBatchNo", ct.c_ulong),        # When byPosMode is LJV7IF_BATCH_POS_SPEC, specifies the batch number for the profiles to get.
		("dwGetProfNo", ct.c_ulong),         # Specifies the profile number for the profiles to get.
		("byGetProfCnt", ct.c_ubyte),         # The number of profiles to read. If the communication buffer is insufficient, the number of profiles specified by byGetProfCnt may not be acquired. In this situation, the maximum number of profiles that can be acquired is returned.
		("reserve", ct.c_ubyte * 3)
	]

class LJV7IF_GET_BATCH_PROFILE_ADVANCE_RSP(ct.Structure):
	_fields_ = [
		("dwGetBatchNo", ct.c_ulong),        # The batch number that was read this time
		("dwGetBatchProfCnt", ct.c_ulong),   # The number of profiles in the batch that was read this time.
		("dwGetBatchTopProfNo", ct.c_ulong), # Indicates what number profile in the batch is the oldest profile out of the profiles that were read this time.
		("byGetProfCnt", ct.c_ubyte),         # The number of profiles that were read this time.
		("reserve", ct.c_ubyte * 3)
	]

class LJV7IF_GET_PROFILE_REQ(ct.Structure):
	_fields_ = [
		("byTargetBank", ct.c_ubyte),
		("byPosMode", ct.c_ubyte),
		("reserve", ct.c_ubyte * 2),
		("dwGetProfNo", ct.c_ulong),
		("byGetProfCnt", ct.c_ubyte),
		("byErase", ct.c_ubyte),
		("reserve", ct.c_ubyte * 2)
	]

class LJV7IF_PROFILE_HEADER(ct.Structure):
	_fields_ = [
		("reserve", ct.c_ulong),             # 7th bit: Indicates whether the encoder's Z phase has been entered. This flag can be used when the controller is version 3.0 or later. This flag is turned ON when Z-phase ON input is received during the period between the previous trigger input (or the start of measurement if there was no previous trigger input) and the current trigger input.
		("dwTriggerCnt", ct.c_ulong),        # Indicates which number trigger from the start of measurements this profile is. (Trigger counter)
		("dwEncoderCnt", ct.c_ulong),        # The encoder count when the trigger was issued. (Encoder counter)
		("reserve2", ct.c_ulong * 3)
	]

class LJV7IF_PROFILE_FOOTER(ct.Structure):
	_fields_ = [
		("reserve", ct.c_ulong)
	]

class LJV7IF_TARGET_SETTING(ct.Structure):
	_fields_ = [
		("byType", ct.c_ubyte),
		("byCategory", ct.c_ubyte),
		("byItem", ct.c_ubyte),
		("reserve", ct.c_ubyte),
		("byTarget1", ct.c_ubyte),
		("byTarget2", ct.c_ubyte),
		("byTarget3", ct.c_ubyte),
		("byTarget4", ct.c_ubyte)
	]

class PROFILE_DATA(ct.Structure):
	_fields_ = [
		("header", LJV7IF_PROFILE_HEADER),
		("data", ct.c_long * 800),
		("footer", LJV7IF_PROFILE_FOOTER)
	]

class BATCH_DATA(ct.Structure):
	_fields_ = [
		("header", LJV7IF_PROFILE_HEADER),
		("data", ct.c_long * 800),
		("footer", LJV7IF_PROFILE_FOOTER),
		("MeasureData", LJV7IF_MEASURE_DATA * 16)
	]

def Initialize(debug = False):
	global DEBUG
	DEBUG = debug
	res = dll.LJV7IF_Initialize()
	if DEBUG: print(f"[Initialize] result: {hex(res)}")
	return res

def GetVersion():
	res = dll.LJV7IF_GetVersion()
	if DEBUG: print(f"[GetVersion] version: {hex(res)}")
	return res

def EthernetOpen(deviceID, ipAddress, port):
	Kconnection = LJV7IF_ETHERNET_CONFIG()
	Kconnection.abyIpAddress[0], Kconnection.abyIpAddress[1], Kconnection.abyIpAddress[2], Kconnection.abyIpAddress[3] = map(lambda x: int(x), ipAddress.split(".", 4))
	Kconnection.wPortNo = port
	res = dll.LJV7IF_EthernetOpen(deviceID, ct.byref(Kconnection))
	if DEBUG: print(f"[EthernetOpen] IP: {ipAddress}, port: {Kconnection.wPortNo}, result: {hex(res)}")
	return res

def SetSetting(deviceID, byType, byCategory, byItem, byTarget1, byTarget2, byTarget3, byTarget4, pData, dwDataSize):
	byDepth = LJV7IF_SETTING_DEPTH_RUNNING # 1 pour running, 2 pour sauvegarder dans ROM
	TargetSetting = LJV7IF_TARGET_SETTING()
	TargetSetting.byType = ct.c_ubyte(byType)
	TargetSetting.byCategory = ct.c_ubyte(byCategory)
	TargetSetting.byItem = ct.c_ubyte(byItem)
	TargetSetting.byTarget1 = ct.c_ubyte(byTarget1)
	TargetSetting.byTarget2 = ct.c_ubyte(byTarget2)
	TargetSetting.byTarget3 = ct.c_ubyte(byTarget3)
	TargetSetting.byTarget4 = ct.c_ubyte(byTarget4)
	pdwError = ct.c_ulong()

	dll.LJV7IF_SetSetting(deviceID, byDepth, TargetSetting, ct.byref(pData), dwDataSize, ct.byref(pdwError))
	if DEBUG: print(f"[SetSetting] setting (type-category-item): {byType}-{byCategory}-{byItem}, result: {hex(pdwError)}")
	return pdwError

def SetSetting_TriggerMode(deviceID, program, mode):
	return SetSetting(deviceID, program + 16, 0, 1, 0, 0, 0, 0, ct.c_ubyte(mode), 1)

def SetSetting_SamplingFrequency(deviceID, program, freq):
	return SetSetting(deviceID, program + 16, 0, 2, 0, 0, 0, 0, ct.c_ubyte(freq), 1)

def SetSetting_BatchMeasurement(deviceID, program, state):
	return SetSetting(deviceID, program + 16, 0, 3, 0, 0, 0, 0, ct.c_ubyte(state), 1)

def GetSetting(deviceID, byType, byCategory, byItem, byTarget1, byTarget2, byTarget3, byTarget4, dwDataSize):
	byDepth = LJV7IF_SETTING_DEPTH_RUNNING # 1 pour running, 2 pour sauvegarder dans ROM
	TargetSetting = LJV7IF_TARGET_SETTING()
	TargetSetting.byType = ct.c_ubyte(byType)
	TargetSetting.byCategory = ct.c_ubyte(byCategory)
	TargetSetting.byItem = ct.c_ubyte(byItem)
	TargetSetting.byTarget1 = ct.c_ubyte(byTarget1)
	TargetSetting.byTarget2 = ct.c_ubyte(byTarget2)
	TargetSetting.byTarget3 = ct.c_ubyte(byTarget3)
	TargetSetting.byTarget4 = ct.c_ubyte(byTarget4)
	pData = ct.c_ulong()
	pdwError = ct.c_ulong()

	dll.LJV7IF_GetSetting(deviceID, byDepth, TargetSetting, ct.byref(pData), dwDataSize, ct.byref(pdwError))
	if DEBUG: print(f"[SetSetting] setting (type-category-item): {byType}-{byCategory}-{byItem}, value: {pData}, result: {hex(pdwError)}")
	return pdwError

def GetSetting_BatchMeasurement(deviceID, program):
	return GetSetting(deviceID, program + 16, 0, 3, 0, 0, 0, 0, 1)

def GetMeasurementValue(deviceID):
	pMeasureData = (LJV7IF_MEASURE_DATA * 16)()
	res = dll.LJV7IF_GetMeasurementValue(deviceID, ct.byref(pMeasureData))
	return 0

def ProfileDataToPointCloud(profileData, y, xStart, xStep):
	return [[(xStart + i * xStep) * RESOLUTION, y, profileData[i] * RESOLUTION] for i in range(len(profileData)) if -48 < profileData[i] * RESOLUTION < 48]

def GetProfileAdvance(deviceID):
	pProfileInfo = LJV7IF_PROFILE_INFO()               # (OUT) The profile information for the acquired profiles   # TODO utiliser les informations contenues dans cette structure
	pdwProfileData = PROFILE_DATA()                    # (OUT) The buffer to get the profile data.
	pMeasureData = (LJV7IF_MEASURE_DATA * 16)()        # (OUT) This buffer stores the data for all 16 OUTs including the OUTs that are not measuring

	res = dll.LJV7IF_GetProfileAdvance(deviceID, ct.byref(pProfileInfo), ct.byref(pdwProfileData), ct.sizeof(pdwProfileData), ct.byref(pMeasureData)) #ct.cast(pMeasureData, ct.POINTER(LJV7IF_MEASURE_DATA))
	if DEBUG: print(f"[GetProfileAdvance] {hex(res)}")
	return ProfileDataToPointCloud(pdwProfileData.data, 0, pProfileInfo.IXStart, pProfileInfo.IXPitch)

def GetBatchProfileAdvance(deviceID, nbProfiles, yStep):
	NB_PROFILES_PER_BATCH = 100
	pReq = LJV7IF_GET_BATCH_PROFILE_ADVANCE_REQ()      # (IN) Specifies the position, etc., of the profiles to get.
	pReq.byPosMode = LJV7IF_BATCH_POS_CURRENT
	pReq.dwGetProfNo = 0
	pReq.byGetProfCnt = NB_PROFILES_PER_BATCH
	pRsp = LJV7IF_GET_BATCH_PROFILE_ADVANCE_RSP()      # (OUT) Indicates the position, etc., of the profiles that were actually acquired.
	pProfileInfo = LJV7IF_PROFILE_INFO()               # (OUT) The profile information for the acquired profiles
	pdwBatchData = (BATCH_DATA * NB_PROFILES_PER_BATCH)()    # (OUT) The buffer to get the profile data. only the number of profiles that could be acquired are returned.
	pBatchMeasureData = (LJV7IF_MEASURE_DATA * 16)()   # (OUT) The measurement results for the batch data that is the target to get. This buffer stores the data for all 16 OUTs including the OUTs that are not measuring.
	pMeasureData = (LJV7IF_MEASURE_DATA * 16)()        # (OUT) The newest measurement results at the time the command was processed. This buffer stores the data for all 16 OUTs including the OUTs that are not measuring. The host requires the passing of a buffer LJV7IF_MEASURE_DATA[16] in size.

	l = []
	currentProfile = 0
	res = dll.LJV7IF_GetBatchProfileAdvance(deviceID, ct.byref(pReq), ct.byref(pRsp), ct.byref(pProfileInfo), ct.byref(pdwBatchData), ct.sizeof(pdwBatchData), ct.byref(pBatchMeasureData), ct.byref(pMeasureData))

	for i in range(0, pRsp.byGetProfCnt):
		l += ProfileDataToPointCloud(pdwBatchData[i].data, yStep * currentProfile, pProfileInfo.IXStart, pProfileInfo.IXPitch)
		currentProfile += 1
	
	if DEBUG: print(f"[GetBatchProfileAdvance] [First batch] batch n°: {pRsp.dwGetBatchNo}, starting at profile n°: {pRsp.dwGetBatchTopProfNo}, number of profiles: {pRsp.byGetProfCnt}, result: {hex(res)}")
	pReq.byPosMode = LJV7IF_BATCH_POS_SPEC
		
	while currentProfile < nbProfiles and pRsp.byGetProfCnt != 0:
		pReq.dwGetBatchNo = pRsp.dwGetBatchNo
		pReq.dwGetProfNo = pRsp.dwGetBatchTopProfNo + pRsp.byGetProfCnt
		res = dll.LJV7IF_GetBatchProfileAdvance(deviceID, ct.byref(pReq), ct.byref(pRsp), ct.byref(pProfileInfo), ct.byref(pdwBatchData), ct.sizeof(pdwBatchData), ct.byref(pBatchMeasureData), ct.byref(pMeasureData))
		for i in range(0, pRsp.byGetProfCnt):
			l += ProfileDataToPointCloud(pdwBatchData[i].data, yStep * currentProfile, pProfileInfo.IXStart, pProfileInfo.IXPitch)
			currentProfile += 1
		
		if DEBUG: print(f"[GetBatchProfileAdvance] [Next batch] batch n°: {pRsp.dwGetBatchNo}, starting at profile n°: {pRsp.dwGetBatchTopProfNo}, number of profiles: {pRsp.byGetProfCnt}, total number of profiles: {currentProfile}, result: {hex(res)}")
	return l

def Trigger(deviceID):
	res = dll.LJV7IF_Trigger(deviceID)
	if DEBUG: print(f"[Trigger] result: {hex(res)}")
	return res

def StartMeasure(deviceID):
	res = dll.LJV7IF_StartMeasure(deviceID)
	if DEBUG: print(f"[StartMeasure] result: {hex(res)}")
	return res

def StopMeasure(deviceID):
	res = dll.LJV7IF_StopMeasure(deviceID)
	if DEBUG: print(f"[StopMeasure] result: {hex(res)}")
	return res

def CommClose(deviceID):
	res = dll.LJV7IF_CommClose(deviceID)
	if DEBUG: print(f"[CommClose] device: {deviceID}, result: {hex(res)}")
	return res

def Finalize():
	res = dll.LJV7IF_Finalize()
	if DEBUG: print(f"[Finalize] result: {hex(res)}")
	return res