import os
import numpy as np
import csv
from pykeyence import *
import math
import time
import open3d as o3d

#############################################################################################
# Script principal
DEVICE_ID = 0
IP_ADDRESS = "10.2.34.1"
PORT = 24691
PROGRAM = 8
FILE_NAME = "nuage.txt"

Initialize(debug = False)
GetVersion()
EthernetOpen(DEVICE_ID, IP_ADDRESS, PORT)

input("Start measure ? [ENTER]")
StartMeasure(DEVICE_ID)

input("Stop Measure ? [ENTER]")
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

file_path = os.path.join(SCRIPT_DIR, FILE_NAME)
pcd = o3d.io.read_point_cloud(file_path, format = 'xyz')
o3d.visualization.draw_geometries([pcd])

# # Set up
# SetSetting_BatchMeasurement(DEVICE_ID, PROGRAM, SETTING_BATCH_MEASUREMENT_OFF)
# SetSetting_SamplingFrequency(DEVICE_ID, PROGRAM, SETTING_SAMPLING_FREQUENCY_200_HZ)
# SetSetting_TriggerMode(DEVICE_ID, PROGRAM, SETTING_TRIGGER_MODE_CONTINUOUS)

CommClose(DEVICE_ID)
Finalize()