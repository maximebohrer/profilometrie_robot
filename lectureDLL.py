import ctypes as ct
import time
# from ctypes import cdll, pointer, create_string_buffer, byref

# Maximum of 200 000 characters
max_buffer_size = 200000

mydll = ct.cdll.LoadLibrary("C:\Profilo\LJV7_IF.dll")

class LJV7IF_ETHERNET_CONFIG(ct.Structure):
        _fields_ = [
            ("abyIpAddress", ct.c_byte * 4),
            ("wPortNo", ct.c_long),
            ("reserve", ct.c_byte * 2)
        ]


Initialize = ct.CFUNCTYPE(ct.c_long)(("LJV7IF_Initialize", mydll))
a = Initialize()
print(a, type(a))

EthernetOpen = ct.CFUNCTYPE(ct.c_long, ct.POINTER(LJV7IF_ETHERNET_CONFIG))(("LJV7IF_EthernetOpen", mydll))

def EthernetConnexion(DeviceID):
    Kconnection = LJV7IF_ETHERNET_CONFIG()

    Kconnection.abyIpAddress[0] = 10
    Kconnection.abyIpAddress[1] = 2
    Kconnection.abyIpAddress[2] = 34
    Kconnection.abyIpAddress[3] = 1
    Kconnection.wPortNo = 24692
    print(f"Connexion à l'adresse IP : {Kconnection.abyIpAddress[0]}.{Kconnection.abyIpAddress[1]}.{Kconnection.abyIpAddress[2]}.{Kconnection.abyIpAddress[3]}, sur le port {Kconnection.wPortNo}")

    res = EthernetOpen(ct.byref(Kconnection), ct.byref(Kconnection))
    return res


DeviceID = 0.0
a = EthernetConnexion(DeviceID)
print(a, type(a))