import ctypes as ct
import time

# codes d'erreur
LJV7IF_RC_OK = 0x0000                       # Normal termination
LJV7IF_RC_ERR_OPEN = 0x1000                 # Failed to open the communication path
LJV7IF_RC_ERR_NOT_OPEN = 0x1001             # The communication path was not established.
LJV7IF_RC_ERR_SEND = 0x1002                 # Failed to send the command.
LJV7IF_RC_ERR_RECEIVE = 0x1003              # Failed to receive a response.
LJV7IF_RC_ERR_TIMEOUT = 0x1004              # A timeout occurred while waiting for the response.
LJV7IF_RC_ERR_NOMEMORY = 0x1005             # Failed to allocate memory.
LJV7IF_RC_ERR_PARAMETER = 0x1006            # An invalid parameter was passed.
LJV7IF_RC_ERR_RECV_FMT = 0x1007             # The received response data was invalid
LJV7IF_RC_ERR_HISPEED_NO_DEVICE = 0x1009    # High-speed communication initialization could not be performed.
LJV7IF_RC_ERR_HISPEED_OPEN_YET = 0x100A     # High-speed communication was initialized.
LJV7IF_RC_ERR_HISPEED_RECV_YET = 0x100B     # Error already occurred during high-speed communication (for high-speed communication)
LJV7IF_RC_ERR_BUFFER_SHORT = 0x100C         # The buffer size passed as an argument is insufficient. 

# Maximum of 200 000 characters
max_buffer_size = 200000

mydll = ct.cdll.LoadLibrary("C:/Users/Maxime/Desktop/profilometrie_robot/LJV7_IF.dll")

class LJV7IF_ETHERNET_CONFIG(ct.Structure):
        _fields_ = [
            ("abyIpAddress", ct.c_byte * 4),
            ("wPortNo", ct.c_short),
            ("reserve", ct.c_byte * 2)
        ]

a = mydll.LJV7IF_Initialize()
print(hex(a))
a = mydll.LJV7IF_GetVersion()
print(hex(a))


def EthernetOpen(deviceId, ipAddress, port):
    Kconnection = LJV7IF_ETHERNET_CONFIG()
    Kconnection.abyIpAddress[0], Kconnection.abyIpAddress[1], Kconnection.abyIpAddress[2], Kconnection.abyIpAddress[3] = map(lambda x: int(x), ipAddress.split(".", 4))
    Kconnection.wPortNo = 24691
    print(f"Connexion à l'adresse IP : {Kconnection.abyIpAddress[0]}.{Kconnection.abyIpAddress[1]}.{Kconnection.abyIpAddress[2]}.{Kconnection.abyIpAddress[3]}, sur le port {Kconnection.wPortNo}")
    res = mydll.LJV7IF_EthernetOpen(deviceId, ct.byref(Kconnection))
    return res

a = EthernetOpen(0, "10.2.34.2", 24691)
print(hex(a))

# autre moyen
# c_Initialize = ct.CFUNCTYPE(ct.c_void_p)(("LJV7IF_Initialize", mydll))
# a = c_Initialize()









