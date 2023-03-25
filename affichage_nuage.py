"""
+------------------------------------------------------------------------+
|                         IMT Nord Europe - 2023                         |
|   BOHRER Maxime, LENTREBECQ Maxime, RUSHENAS Arnaud, TRAMAILLE Robin   |
+------------------------------------------------------------------------+

Affichage d'un nuage de points avec Open3D. Modifier le fichier à la ligne 12
"""

import open3d as o3d

FILE_NAME = "data/nuage0.txt"

# Chargement du nuage de points
pcd = o3d.io.read_point_cloud(FILE_NAME, format = 'xyz')

# Création de la boîte englobante
bbox = pcd.get_axis_aligned_bounding_box()

# Création de l'objet représentant les axes
mesh_frame = o3d.geometry.TriangleMesh.create_coordinate_frame(size = 16, origin = [0, 0, 0])

# Création de la fenêtre de visualisation et ajout des géométries
visualizer = o3d.visualization.Visualizer()
visualizer.create_window()

visualizer.add_geometry(pcd)
visualizer.add_geometry(mesh_frame)

# Affichage de la fenêtre de visualisation
visualizer.run()