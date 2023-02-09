import ctypes as ct
import time

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

# Maximum of 200 000 characters
max_buffer_size = 200000

mydll = ct.cdll.LoadLibrary("C:/Users/profilometre/Desktop/profilometrie_robot/LJV7_IF.dll")

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

def HighSpeedDataEthernetCommunicationInitialize(deviceID, ipAddress, port):
	data = 0
	def mafonctioncallback(pBuffer, dwSize, dwCount, dwNotify, dwUser):
		print(pBuffer)
	prototype = ct.CFUNCTYPE(ct.c_void_p, #ct.byref(ct.c_byte),
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

def CommClose(deviceID):
	res = mydll.LJV7IF_CommClose(deviceID)
	print(f"Fin de la connexion avec device {deviceID} : {hex(res)}")
	return res

def Finalize():
	res = mydll.LJV7IF_Finalize()
	print(f"Finalisation du DLL : {hex(res)}")
	return res

#############################################################################################
# Script principal
deviceID = 0
ipAddress = "10.2.34.1"
port = 24691
portHighSpeed = 24692

Initialize()
GetVersion()
EthernetOpen(deviceID, ipAddress, port)
HighSpeedDataEthernetCommunicationInitialize(deviceID, ipAddress, portHighSpeed) # Pas finie, callback function in there

bySendPos = 0


pProfileInfo = PreStartHighSpeedDataCommunication(deviceID, bySendPos)
StartHighSpeedDataCommunication(deviceID)

StopHighSpeedDataCommunication(deviceID)
HighSpeedDataCommunicationFinalize(deviceID)


input("Fin de la sim ? [ENTER]")
CommClose(deviceID)
Finalize()