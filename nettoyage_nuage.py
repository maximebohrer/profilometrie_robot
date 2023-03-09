# Step 1 & 2: Setting up the environment and loading the data
#libraries used
import numpy as np
import open3d as o3d
import matplotlib.pyplot as plt
import os

#create paths and load data
FILE_NAME = "data/nuage_pour_les_gars.txt"
SCRIPT_DIR = os.path.dirname(__file__)
file_path = os.path.join(SCRIPT_DIR, FILE_NAME)

pcd = o3d.io.read_point_cloud(file_path, format = 'xyz')

"""# Step 3: First segmentation round
## 3.1 [Optional] Normals computation
"""

pcd.estimate_normals(search_param = o3d.geometry.KDTreeSearchParamHybrid(radius = 0.1,
                                                                         max_nn = 16),
                     fast_normal_computation = True)
pcd.paint_uniform_color([0.6, 0.6, 0.6])
#o3d.visualization.draw_geometries([pcd]) #Works only outside Jupyter/Colab

"""## 3.2 [INITIATION] 3D Shape Detection with RANSAC"""

# plane_model, inliers = pcd.segment_plane(distance_threshold=0.01,ransac_n=3,num_iterations=1000)
# [a, b, c, d] = plane_model
# print(f"Plane equation: {a:.2f}x + {b:.2f}y + {c:.2f}z + {d:.2f} = 0")
# inlier_cloud = pcd.select_by_index(inliers)
# outlier_cloud = pcd.select_by_index(inliers, invert=True)
# inlier_cloud.paint_uniform_color([1.0, 0, 0])
# outlier_cloud.paint_uniform_color([0.6, 0.6, 0.6])
# o3d.visualization.draw_geometries([inlier_cloud, outlier_cloud])

"""## 3.3 [INITIATION] Clustering with DBSCAN"""

# labels = np.array(pcd.cluster_dbscan(eps=0.05, min_points=10))
# max_label = labels.max()
# print(f"point cloud has {max_label + 1} clusters")

# colors = plt.get_cmap("tab20")(labels / (max_label if max_label > 0 else 1))
# colors[labels < 0] = 0
# pcd.colors = o3d.utility.Vector3dVector(colors[:, :3])

# o3d.visualization.draw_geometries([pcd])

"""# Step 4: Scaling and automation
## 4.1 RANSAC loop for multiple planar shapes detection with Euclidean clustering
"""

segment_models                  = {}
segments                        = {}
max_plane_idx                   = 10
rest                            = pcd

d_threshold_segment_plane       = 0.5
ransac_n_segment_plane          = 3
num_iterations_segment_plane    = 1000

d_threshold_cluster_dbscan      = 1
min_points_cluster_dbscan       = 10

for i in range(max_plane_idx):
    colors = plt.get_cmap("tab20")(i)
    segment_models[i], inliers = rest.segment_plane(distance_threshold  = d_threshold_segment_plane, # Max distance a point can be from the plane model and still be considered an inlier
                                                    ransac_n            = ransac_n_segment_plane, # Number of initial points to be considered inliers in each iteration
                                                    num_iterations      = num_iterations_segment_plane) # Number of iterations
    segments[i] = rest.select_by_index(inliers)
    
    print("Enterring cluster_dbscan")
    labels = np.array(segments[i].cluster_dbscan(eps        = d_threshold_cluster_dbscan, # Density parameter used to find neighbouring points
                                                 min_points = min_points_cluster_dbscan, # Minimum number of points to form a cluster
                                                 print_progress = True))
    print("Exiting cluster_dbscan")
    
    candidates = [len(np.where(labels == j)[0]) for j in np.unique(labels)]
    print(f"Labels {labels}\nnp.unique... {np.unique(labels)}")
    print(f"Candidats {candidates}, np... {np.where(candidates == np.max(candidates))[0]}")

    best_candidate = int(np.unique(labels)[np.where(candidates == np.max(candidates))[0]])
    print(f"The best candidate is : {best_candidate}")
    rest = rest.select_by_index(inliers, invert = True) + segments[i].select_by_index(list(np.where(labels != best_candidate)[0]))
    segments[i] = segments[i].select_by_index(list(np.where(labels == best_candidate)[0]))
    segments[i].paint_uniform_color(list(colors[:3]))
    print(f"Pass {i + 1} / {max_plane_idx} done")

"""## 4.2 Euclidean clustering of the rest with DBSCAN"""

labels = np.array(rest.cluster_dbscan(eps = 0.05, min_points = 5))
max_label = labels.max()
print(f"Point cloud has {max_label + 1} clusters")

colors = plt.get_cmap("tab10")(labels / (max_label if max_label > 0 else 1))
colors[labels < 0] = 0
rest.colors = o3d.utility.Vector3dVector(colors[:, :3])

# o3d.visualization.draw_geometries([segments.values()])
# o3d.visualization.draw_geometries([segments[i] for i in range(max_plane_idx)]+[rest])
#o3d.visualization.draw_geometries([segments[i] for i in range(max_plane_idx)]+[rest],zoom=0.3199,front=[0.30159062875123849, 0.94077325609922868, 0.15488309545553303],lookat=[-3.9559999108314514, -0.055000066757202148, -0.27599999308586121],up=[-0.044411423633999815, -0.138726419067636, 0.98753122516983349])
# o3d.visualization.draw_geometries([rest])
exit()
"""# BONUS: Small drawing function for Colab"""

from mpl_toolkits import mplot3d

pc = np.asarray(pcd.points)
ax = plt.axes(projection='3d')
ax.scatter(pc[:,0], pc[:,1], pc[:,2], c = np.asarray(pcd.colors), s=0.01)
plt.show()