import ctypes as ct
import time
# from ctypes import cdll, pointer, create_string_buffer, byref

# Maximum of 200 000 characters
max_buffer_size = 200000

mydll = ct.cdll.LoadLibrary("C:/Users/profilometre/Desktop/profilometrie_robot/LJV7_IF.dll")

class LJV7IF_ETHERNET_CONFIG(ct.Structure):
        _fields_ = [
            ("abyIpAddress", ct.c_byte * 4),
            ("wPortNo", ct.c_short),
            ("reserve", ct.c_byte * 2)
        ]

class LJV7IF_ETHERNET_CONFIG_DEVICE_ID(ct.Structure):
        _fields_ = [
            ("ID", ct.c_long)
        ]


c_Initialize = ct.CFUNCTYPE(ct.c_void_p)(("LJV7IF_Initialize", mydll))
c_EthernetOpen = ct.CFUNCTYPE(ct.c_long, ct.POINTER(LJV7IF_ETHERNET_CONFIG))(("LJV7IF_EthernetOpen", mydll))
c_GetVersion = ct.CFUNCTYPE(ct.c_void_p)(("LJV7IF_GetVersion", mydll))

a = c_Initialize()
print(a, type(a))
a = c_GetVersion()
print(a, type(a))


def EthernetOpen():
    DeviceID = LJV7IF_ETHERNET_CONFIG_DEVICE_ID()
    DeviceID.ID = 0

    Kconnection = LJV7IF_ETHERNET_CONFIG()
    Kconnection.abyIpAddress[0] = 10
    Kconnection.abyIpAddress[1] = 2
    Kconnection.abyIpAddress[2] = 34
    Kconnection.abyIpAddress[3] = 1
    Kconnection.wPortNo = 24691
    print(f"Connexion à l'adresse IP : {Kconnection.abyIpAddress[0]}.{Kconnection.abyIpAddress[1]}.{Kconnection.abyIpAddress[2]}.{Kconnection.abyIpAddress[3]}, sur le port {Kconnection.wPortNo}")

    res = c_EthernetOpen(ct.byref(Kconnection))
    return res


a = EthernetOpen()
print(a, type(a))








#define LJV7IF_RC_OK						0x0000	// Normal termination
#define LJV7IF_RC_ERR_OPEN					0x1000	// Failed to open the communication path
#define LJV7IF_RC_ERR_NOT_OPEN				0x1001	// The communication path was not established.
#define LJV7IF_RC_ERR_SEND					0x1002	// Failed to send the command.
#define LJV7IF_RC_ERR_RECEIVE				0x1003	// Failed to receive a response.
#define LJV7IF_RC_ERR_TIMEOUT				0x1004	// A timeout occurred while waiting for the response.
#define LJV7IF_RC_ERR_NOMEMORY				0x1005	// Failed to allocate memory.
#define LJV7IF_RC_ERR_PARAMETER				0x1006	// An invalid parameter was passed.
#define LJV7IF_RC_ERR_RECV_FMT				0x1007	// The received response data was invalid

#define LJV7IF_RC_ERR_HISPEED_NO_DEVICE		0x1009	// High-speed communication initialization could not be performed.
#define LJV7IF_RC_ERR_HISPEED_OPEN_YET		0x100A	// High-speed communication was initialized.
#define LJV7IF_RC_ERR_HISPEED_RECV_YET		0x100B	// Error already occurred during high-speed communication (for high-speed communication)
#define LJV7IF_RC_ERR_BUFFER_SHORT			0x100C	// The buffer size passed as an argument is insufficient. 

