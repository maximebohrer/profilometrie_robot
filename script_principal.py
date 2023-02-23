import time
from pykuka import *
from pykeyence import *

send_kuka_3964R_single_char(POS)              # send POS signal to request position
p = read_kuka_3964R_pose()                    # read position
print(p)

new_home = Pose(0, 370.02, 614.98, -180, 0, -180) # Without tool, in base NULLFRAME
pose_recup = Pose(353, 300, 358.5, -88.5, 88.5, 82.3)
pose_recup_loin = pose_recup.copy()
pose_recup_loin.z += 50

kuka_go_to_pose(new_home) # Home

kuka_go_to_pose(pose_recup_loin) # Dessus tapis loin

kuka_go_to_pose(pose_recup) # Dessus tapis proche

send_kuka_3964R_single_char(GRAB) # Grab

kuka_go_to_pose(pose_recup_loin) # Dessus tapis loin

kuka_go_to_pose(new_home) # Back home

send_kuka_3964R_single_char(DROP) # Drop

# for i in range(10):
#     p.y += 2
#     kuka_go_to_pose(p)
#     time.sleep(0.5)