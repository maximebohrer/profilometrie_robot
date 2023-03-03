import time
from pykuka import *
from pykeyence import *
from transformations import *
# import open3d as o3d
import os

DEVICE_ID   = 0
IP_ADDRESS  = "10.2.34.1"
PORT        = 24691
PROGRAM     = 8
vitesse_robot       = 0.0065 # m/s
frequence_profilo   = 50 # Hz
yStep = vitesse_robot * 1000 / frequence_profilo # mm/s
base_point_cloud_dans_base_profilo = get_htm(-2.5, -10, -170, 0, 0, 0)

Initialize(debug = True)
initialize("COM1")
GetVersion()
EthernetOpen(DEVICE_ID, IP_ADDRESS, PORT)

send_3964R_single_char(GO)

f = open("data/nuage.txt", 'w')
f_brut = open("data/nuage_brut.txt", 'w')

while True:
    go = read_3964R_single_char()
    if go != GO:
        break
    pose = read_3964R_pose()
    print(f"Position de départ : {pose}")
    StartMeasure(DEVICE_ID)
    done = read_3964R_single_char()
    StopMeasure(DEVICE_ID)

    point_cloud = GetBatchProfileAdvance(DEVICE_ID, 100, 1000, -yStep)

    base_outil_dans_base_profilo = get_htm(pose.x, pose.y, pose.z, pose.a, pose.b, pose.c)
    base_profilo_dans_base_outil = base_outil_dans_base_profilo.I
    base_point_cloud_dans_base_outil = base_profilo_dans_base_outil * base_point_cloud_dans_base_profilo

    points_dans_base_outil = apply_htm(base_point_cloud_dans_base_outil, point_cloud)

    f_brut.write(pose.to_string() + "\n")
    for i in len(point_cloud):
        f.write(str(points_dans_base_outil[i][0]) + "\t" + str(points_dans_base_outil[i][1]) + "\t" + str(points_dans_base_outil[i][2]) + "\n")
        f_brut.write(str(point_cloud[i][0]) + "\t" + str(point_cloud[i][1]) + "\t" + str(point_cloud[i][2]) + "\n")
    f_brut.write("**********\n")

f.close()
CommClose(DEVICE_ID)
Finalize()
finalize()

# file_path = os.path.join(SCRIPT_DIR, FILE_NAME)
# pcd = o3d.io.read_point_cloud(file_path, format = 'xyz')
# o3d.visualization.draw_geometries([pcd])

