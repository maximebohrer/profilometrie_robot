import serial
serial.Serial()

import os
import open3d as o3d
import numpy as np
from pykuka import Pose
import transformations as trans

base_point_cloud_dans_base_profilo = trans.get_htm(-2.5, -10, -170, 0, 0, 0)

f_brut = open("data/nuage_brut.txt", 'r')
f = open("data/nuage.txt", 'w')

line = f_brut.readline().strip()
while line != "":
    pose = Pose.from_string(line)
    face = []
    line = f_brut.readline().strip()

    while line != "**********":
        split = line.split("\t")
        face.append([float(split[0]), float(split[1]), float(split[2])])
        line = f_brut.readline().strip()
    
    base_outil_dans_base_profilo = trans.get_htm(pose.x, pose.y, pose.z, pose.a, pose.b, pose.c)
    base_profilo_dans_base_outil = base_outil_dans_base_profilo.I
    base_point_cloud_dans_base_outil = base_profilo_dans_base_outil * base_point_cloud_dans_base_profilo
    
    points_dans_base_outil = trans.apply_htm(base_point_cloud_dans_base_outil, face)

    for item in points_dans_base_outil:
        f.write(str(item[0]) + "\t" + str(item[1]) + "\t" + str(item[2]) + "\n")

    line = f_brut.readline().strip()

f.close()

# visualiser nuage
import lecture_nuage