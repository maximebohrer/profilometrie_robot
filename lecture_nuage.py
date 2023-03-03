import os
import open3d as o3d
import numpy as np

# x selon axe rouge
# y selon axes rouge et -vert
# z selon axe -rouge et -vert

FILE_NAME = "data/nuage.txt"
SCRIPT_DIR = os.path.dirname(__file__)

file_path = os.path.join(SCRIPT_DIR, FILE_NAME)

# Chargement du nuage de points
pcd = o3d.io.read_point_cloud(file_path, format = 'xyz')

# Création de la boîte englobante
bbox = pcd.get_axis_aligned_bounding_box()

# Création de l'objet représentant les axes
mesh_frame = o3d.geometry.TriangleMesh.create_coordinate_frame(size = 16, origin = [0, 0, 0])

# Transformation de la boîte englobante pour représenter les axes
# mesh_frame.rotate(np.array([[1, 0, 0], [0, -1, 0], [0, 0, -1]]), center = [0, 0, 0])
# mesh_frame.translate([bbox.max_bound[0], bbox.max_bound[1], bbox.max_bound[2]])

# Création de la fenêtre de visualisation et ajout des géométries
visualizer = o3d.visualization.Visualizer()
visualizer.create_window()

visualizer.add_geometry(pcd)
visualizer.add_geometry(mesh_frame)

# Affichage de la fenêtre de visualisation
visualizer.run()