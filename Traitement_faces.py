import open3d as o3d
import numpy as np
import csv
import os
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from mpl_toolkits.mplot3d import Axes3D
from scipy.linalg import lstsq
import matplotlib.lines as mlines

def calculate_side_length(corner1, corner2):
    return np.linalg.norm(np.array(corner1) - np.array(corner2))

# Function to calculate the plane equation using 4 points
def calculate_plane_equation(p1, p2, p3, p4):
    A = np.vstack([p1, p2, p3, p4])
    b = np.ones(4)
    coeff, _, _, _ = lstsq(A, b)
    D = -1  # D is -1 since we set b to be an array of ones
    return np.append(coeff, D)

def separate_points_by_faces(points, plane_equations, tolerance):
    face_points = [[] for _ in range(6)]
    
    for point in points:
        for i, plane in enumerate(plane_equations):
            A, B, C, D = plane
            x, y, z = point
            distance = abs(A * x + B * y + C * z + D)
            
            if distance <= tolerance:
                face_points[i].append(point)
                break
    
    return face_points

def calculate_roughness(face_points, plane):
    A, B, C, D = plane
    distances = [abs(A * x + B * y + C * z + D) / np.sqrt(A**2 + B**2 + C**2) for x, y, z in np.array(face_points)]
    roughness = max(distances) - min(distances)
    return roughness

def resolve_equations(sides, user_dimensions):    
    side_lengths = {}
    for i, side_group in enumerate(side_names):
        for side in side_group:
            side_lengths[side] = user_dimensions[i]
    
    return side_lengths


#CALCUL DES COINS ET SEPARATION DES FACES
# Load point cloud
file_path = 'Data/Raw/nuage0.txt'
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

#Load point cloud
pcd = o3d.io.read_point_cloud(file_path, format="xyz")

npCornerA = np.array(cornerA)
npCornerB = np.array(cornerB)
npCornerC = np.array(cornerC)
npCornerD = np.array(cornerD)
npCornerE = np.array(cornerE)
npCornerF = np.array(cornerF)
npCornerG = np.array(cornerG)
npCornerH = np.array(cornerH)

# Define cube faces
faces = [
    [npCornerA, npCornerB, npCornerC, npCornerD],  # face ABCD
    [npCornerA, npCornerD, npCornerH, npCornerE],  # face AEHD
    [npCornerA, npCornerB, npCornerF, npCornerE],  # face ABFE
    [npCornerB, npCornerC, npCornerG, npCornerF],  # face BCGF
    [npCornerC, npCornerD, npCornerH, npCornerG],  # face CDHG
    [npCornerE, npCornerF, npCornerG, npCornerH]   # face EFGH
]


# Calculate plane equations for each face
plane_equations = []
for face in faces:
    plane_equation = calculate_plane_equation(face[0], face[1], face[2], face[3])
    plane_equations.append(plane_equation)

for i, plane in enumerate(plane_equations):
    print(f"Face {i+1}: {plane[0]:.10f}x + {plane[1]:.10f}y + {plane[2]:.10f}z + {plane[3]:.10f} = 0")
    
#split the point cloud per face
points_by_face = separate_points_by_faces(points, plane_equations, 0.07)

# Create an empty point cloud
pcd = o3d.geometry.PointCloud()

colors = [
    [1, 0, 0],  # red
    [0, 0, 1],  # blue
    [0, 1, 0],  # green
    [1, 1, 0],  # yellow
    [0, 1, 1],  # cyan
    [1, 0, 1],  # magenta
]

# Add points and colors for each face
for face_points, color in zip(points_by_face, colors):
    face_points = np.array(face_points)
    if face_points.ndim == 2 and face_points.shape[1] == 3:
        pcd.points.extend(o3d.utility.Vector3dVector(face_points))
        pcd.colors.extend([color] * len(face_points))
    else:
        print(f"Face has incorrect format: {face_points}")

# Visualize the point cloud to verify clustering
#o3d.visualization.draw_geometries([pcd])

#CALCUL DES DIMENSIONS ET ANALYSE DE SURFACE
# Exemple de dimensions définies par l'utilisateur
side_names = [
        ["A-D", "H-E", "B-C", "G-F"],
        ["E-A", "D-H", "C-G", "F-B"],
        ["E-F", "B-A", "C-D", "H-G"]
    ]
user_dimensions = [65, 65, 50]
expected_lengths = resolve_equations(side_names, user_dimensions)
tolerance = 5

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
    
    # Calculer la rugosité de la face avec la fonction calculate_roughness
    points = np.asarray(pcd.points)
    plane_equation = plane_equations[i]  # Get the corresponding plane equation for the face
    points_by_face  
    roughness = calculate_roughness(np.asarray(points_by_face[i]), plane_equation)

    
    # Afficher les informations de la face
    face_name = ''.join(face_corners[i])
    print("Face {} - Aire : {:.2f}mm^2 / Rugosité : {:.3f}mm : ".format(face_name, area, roughness))
    print("{}-{} : {:.2f}mm".format(face_corners[i][0], face_corners[i][1], side_lengths[0]), "/ {}-{} : {:.2f}mm".format(face_corners[i][2], face_corners[i][3], side_lengths[2]))
    print("{}-{} : {:.2f}mm".format(face_corners[i][1], face_corners[i][2], side_lengths[1]), "/ {}-{} : {:.2f}mm".format(face_corners[i][3], face_corners[i][0], side_lengths[3]),"\n")


        
#AFFICHAGE DES COINS CALCULES ET DU CUBE - DEBUG    
A = tuple(cornerA)
B = tuple(cornerB)
C = tuple(cornerC)
D = tuple(cornerD)
E = tuple(cornerE)
F = tuple(cornerF)
G = tuple(cornerG)
H = tuple(cornerH)

points = [A, B, C, D, E, F, G, H]

faces = [
    [A, B, C, D],  # face ABCD
    [A, D, H, E],  # face AEHD
    [A, B, F, E],  # face ABFE
    [B, C, G, F],  # face BCGF
    [C, D, H, G],  # face CDHG
    [E, F, G, H]   # face EFGH
]

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

ax.set_xlim3d([-65, 100])
ax.set_ylim3d([-100, 100])
ax.set_zlim3d([-100, 100])

ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')

plt.show()