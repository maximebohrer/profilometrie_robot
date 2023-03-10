import os
import open3d as o3d
import numpy as np
from transformations import *

# x selon axe rouge
# y selon axes rouge et -vert
# z selon axe -rouge et -vert

FILE_NAME = "data/nuage0.txt"
SCRIPT_DIR = os.path.dirname(__file__)

file_path = os.path.join(SCRIPT_DIR, FILE_NAME)

# Chargement du nuage de points
pcd = o3d.io.read_point_cloud(file_path, format = 'xyz')

# Création de la boîte englobante
bbox = pcd.get_axis_aligned_bounding_box()
base_point_cloud_dans_base_profilo = get_htm(+0, +15, -155, 0, 0, 0)
base_outil_dans_base_profilo = get_htm(24.91, -87.10, -207.03, -148.35, -34.02, 94.12)
base_profilo_dans_base_outil = base_outil_dans_base_profilo.I
base_point_cloud_dans_base_outil = base_profilo_dans_base_outil * base_point_cloud_dans_base_profilo
base_outil_dans_base_point_cloud = base_point_cloud_dans_base_outil.I

# Création de l'objet représentant les axes
mesh_frame = o3d.geometry.TriangleMesh.create_coordinate_frame(size = 16, origin = [0, 0, 0])
mesh_frame2 = o3d.geometry.TriangleMesh.create_coordinate_frame(size = 16, origin = apply_htm(base_outil_dans_base_point_cloud, [0,0,0]).tolist()[0])

# Transformation de la boîte englobante pour représenter les axes
# mesh_frame.rotate(np.array([[1, 0, 0], [0, -1, 0], [0, 0, -1]]), center = [0, 0, 0])
# mesh_frame.translate([bbox.max_bound[0], bbox.max_bound[1], bbox.max_bound[2]])

# Création de la fenêtre de visualisation et ajout des géométries
visualizer = o3d.visualization.Visualizer()
visualizer.create_window()

visualizer.add_geometry(pcd)
visualizer.add_geometry(mesh_frame)
visualizer.add_geometry(mesh_frame2)

# Affichage de la fenêtre de visualisation
visualizer.run()