import time
from pykuka import *
from pykeyence import *
# import open3d as o3d
import os

DEVICE_ID   = 0
IP_ADDRESS  = "10.2.34.1"
PORT        = 24691
PROGRAM     = 8
FILE_NAME   = "nuage.txt"

Initialize(debug = True)
GetVersion()
EthernetOpen(DEVICE_ID, IP_ADDRESS, PORT)

#send_3964R_single_char(GO)

go = read_3964R_single_char()

if go != GO: exit()

pose = read_3964R_pose()
print(f"Position de départ : {pose}")

StartMeasure(DEVICE_ID)

done = read_3964R_single_char()

while done != DONE:
    done = read_3964R_single_char()

StopMeasure(DEVICE_ID)


NB_PROF_PAR_LOT = 10
LIM_NB_PROF = 1000
yStep = 0.1

cloud = GetBatchProfileAdvance(DEVICE_ID, NB_PROF_PAR_LOT, LIM_NB_PROF, yStep)


# Visualisation 3D du profile
FILE_NAME = "nuage.txt"
SCRIPT_DIR = os.path.dirname(__file__)

f = open(FILE_NAME, 'w')
for item in cloud:
    f.write(str(item[0]) + "\t" + str(item[1]) + "\t" + str(item[2]) + "\n")
f.close()

# file_path = os.path.join(SCRIPT_DIR, FILE_NAME)
# pcd = o3d.io.read_point_cloud(file_path, format = 'xyz')
# o3d.visualization.draw_geometries([pcd])

CommClose(DEVICE_ID)
Finalize()