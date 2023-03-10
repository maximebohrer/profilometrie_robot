from pykeyence import *
from transformations import *

vitesse_robot       = 0.0130 # m/s
frequence_profilo   = 100 # Hz
yStep = vitesse_robot * 1000 / frequence_profilo # mm
DEVICE_ID   = 0
IP_ADDRESS  = "10.2.34.1"
PORT        = 24691

Initialize(debug = True)
EthernetOpen(DEVICE_ID, IP_ADDRESS, PORT)
input("Start ?")
StartMeasure(DEVICE_ID)
input("Stop ?")
StopMeasure(DEVICE_ID)
point_cloud = GetBatchProfileAdvance(DEVICE_ID, 100, 1000, -yStep)

with open("data/beton_brut.txt", 'w') as f_brut:
    for i in point_cloud:
        f_brut.write(f"{i[0]}\t{i[1]}\t{i[2]}\n")