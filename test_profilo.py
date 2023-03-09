from pykeyence import *
from transformations import *

vitesse_robot       = 0.0065 # m/s
frequence_profilo   = 50 # Hz
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

with open("data/nuage_brut.txt", 'w') as f_brut:
    for i in point_cloud:
        f_brut.write(f"{i[0]}\t{i[1]}\t{i[2]}\n")

base_point_cloud_dans_base_profilo = get_htm(+0, +15, -170, 0, 0, 0)

base_outil_dans_base_profilo = get_htm(-18.80, -81.78, -209.78, 138.74, -34.05, 94.13)
base_profilo_dans_base_outil = base_outil_dans_base_profilo.I
base_point_cloud_dans_base_outil = base_profilo_dans_base_outil * base_point_cloud_dans_base_profilo
points_dans_base_outil = apply_htm(base_point_cloud_dans_base_outil, point_cloud)

with open("data/nuage.txt", 'w') as f_brut:
    for i in points_dans_base_outil:
        f_brut.write(f"{i[0]}\t{i[1]}\t{i[2]}\n")