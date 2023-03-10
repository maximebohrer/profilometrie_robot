import open3d as o3d
import numpy as np
import csv
import os
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

def calculate_side_length(corner1, corner2):
    return np.linalg.norm(np.array(corner1) - np.array(corner2))

# Load point cloud
file_path = 'Data/Raw/nuage_angles_method2.txt'
with open(file_path, 'r') as f:
    lines = f.readlines()
filtered_lines = []
i = 0
for line in lines:
    if float(line.split()[2]) >= 6 and i % 2 == 0:
        filtered_lines.append(line)
    i += 1
pcd = o3d.geometry.PointCloud()
pcd.points = o3d.utility.Vector3dVector(np.asarray([list(map(float, row.split())) for row in filtered_lines]))

# Test different combinations of nb_neighbors and std_ratio
nb_neighbors_values = 30
std_ratio_values = 2

# Remove statistical outliers with current parameter values
pcd_filtered, _ = pcd.remove_statistical_outlier(nb_neighbors_values, std_ratio_values)

# Save point cloud as text file
points = np.asarray(pcd_filtered.points)
filename = f"Data/Debug/nuage_filtered_outliers_removed_{nb_neighbors_values}_{std_ratio_values}.txt"
np.savetxt(filename, points, delimiter='\t', fmt='%.8f')

# Define cube corners
list_points = np.asarray(pcd_filtered.points)

plus_x_plus_y_moins_z = list(map(lambda p: p[0]+p[1]-p[2], list_points))
cornerC = list_points[plus_x_plus_y_moins_z.index(max(plus_x_plus_y_moins_z))] 
cornerE = list_points[plus_x_plus_y_moins_z.index(min(plus_x_plus_y_moins_z))]

plus_x_plus_y_plus_z = list(map(lambda p: p[0]+p[1]+p[2], list_points))
cornerG = list_points[plus_x_plus_y_plus_z.index(max(plus_x_plus_y_plus_z))] 
cornerA = list_points[plus_x_plus_y_plus_z.index(min(plus_x_plus_y_plus_z))]

plus_x_moins_y_plus_z = list(map(lambda p: p[0]-p[1]+p[2], list_points))
cornerH = list_points[plus_x_moins_y_plus_z.index(max(plus_x_moins_y_plus_z))] 
cornerB = list_points[plus_x_moins_y_plus_z.index(min(plus_x_moins_y_plus_z))] 

plus_x_moins_y_moins_z = list(map(lambda p: p[0]-p[1]-p[2], list_points))
cornerD = list_points[plus_x_moins_y_moins_z.index(max(plus_x_moins_y_moins_z))] 
cornerF = list_points[plus_x_moins_y_moins_z.index(min(plus_x_moins_y_moins_z))] 

# Charger le nuage de points
pcd = o3d.io.read_point_cloud(file_path, format="xyz")

npCornerA = np.array(cornerA)
npCornerB = np.array(cornerB)
npCornerC = np.array(cornerC)
npCornerD = np.array(cornerD)
npCornerE = np.array(cornerE)
npCornerF = np.array(cornerF)
npCornerG = np.array(cornerG)
npCornerH = np.array(cornerH)
     
# Définir les faces du cube en fonction des coins
faces = [
    [npCornerA, npCornerB, npCornerC, npCornerD],  # face ABCD
    [npCornerA, npCornerD, npCornerH, npCornerE],  # face AEHD
    [npCornerA, npCornerB, npCornerF, npCornerE],  # face ABFE
    [npCornerB, npCornerC, npCornerG, npCornerF],  # face BCGF
    [npCornerC, npCornerD, npCornerH, npCornerG],  # face CDHG
    [npCornerE, npCornerF, npCornerG, npCornerH]   # face EFGH
]

file_path_corner = "Data/corners.txt"
fichier_corners = open(file_path_corner, 'w')
corners = csv.writer(fichier_corners, delimiter='\t')

face_corners = [['A', 'B', 'C', 'D'], ['E', 'A', 'D', 'H'], ['B', 'A', 'E', 'F'], ['F', 'B', 'C', 'G'], ['F', 'E', 'H', 'G'], ['C', 'D', 'H', 'G']]

for i, face in enumerate(faces):
    # Calculer la longueur de chaque côté de la face
    side_lengths = []
    for j in range(len(face)):
        current_corner = face[j]
        next_corner = face[(j+1)%len(face)]
        side_lengths.append(np.linalg.norm(next_corner - current_corner))
    
    # Calculer l'aire de la face
    s = sum(side_lengths) / 2
    area = np.sqrt(s * (s - side_lengths[0]) * (s - side_lengths[1]) * (s - side_lengths[2]))
    
    # Calculer la rugosité de la face
    points = np.asarray(pcd.points)
    face_points = np.array([points.tolist().index(corner.tolist()) for corner in face])
    dists = np.sqrt(np.sum((points[face_points] - np.mean(points[face_points], axis=0)) ** 2, axis=1))
    roughness = np.max(dists) - np.min(dists)
    
    # Afficher les informations de la face
    face_name = ''.join(face_corners[i])
    print("Face {} - Aire : {:.2f}mm^2 / Rugosité : {:.2f}mm : ".format(face_name, area, roughness))
    print("{}-{} : {:.2f}mm".format(face_corners[i][0], face_corners[i][1], side_lengths[0]), "/ {}-{} : {:.2f}mm".format(face_corners[i][2], face_corners[i][3], side_lengths[2]))
    print("{}-{} : {:.2f}mm".format(face_corners[i][1], face_corners[i][2], side_lengths[1]), "/ {}-{} : {:.2f}mm".format(face_corners[i][3], face_corners[i][0], side_lengths[3]),"\n")

with fichier_corners as f:
    for corner in [cornerA, cornerB, cornerC, cornerD, cornerE, cornerF, cornerG, cornerH]:
        f.write("\t".join(str(coord) for coord in corner) + "\n")

# Les points du cube
A = tuple(cornerA)
B = tuple(cornerB)
C = tuple(cornerC)
D = tuple(cornerD)
E = tuple(cornerE)
F = tuple(cornerF)
G = tuple(cornerG)
H = tuple(cornerH)

# La liste des points
points = [A, B, C, D, E, F, G, H]

# Les faces du cube
faces = [
    [A, B, C, D],  # face ABCD
    [A, D, H, E],  # face AEHD
    [A, B, F, E],  # face ABFE
    [B, C, G, F],  # face BCGF
    [C, D, H, G],  # face CDHG
    [E, F, G, H]   # face EFGH
]

# Affichage du cube
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

for i, point in enumerate(points):
    ax.scatter(point[0], point[1], point[2])
    ax.text(point[0], point[1], point[2], "{}".format(chr(65+i)), fontsize=12)

for face in faces:
    x = [point[0] for point in face]
    y = [point[1] for point in face]
    z = [point[2] for point in face]
    verts = [list(zip(x, y, z))]
    ax.add_collection3d(Poly3DCollection(verts, alpha=0.25, facecolor='blue', linewidths=1, edgecolors='black'))

ax.set_xlim3d([-100, 100])
ax.set_ylim3d([-100, 100])
ax.set_zlim3d([-100, 100])

ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')

plt.show()