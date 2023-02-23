import time
from pykuka import *
from pykeyence import *

send_kuka_3964R_single_char(POS)              # send POS signal to request position
p = read_kuka_3964R_pose()                    # read position
print(p)

new_home = Pose(0, 370.02, 614.98, -180, 0, -180) # Without tool, in base NULLFRAME

pose_recup = Pose(350.86, 300.52, 430.88, 76.82, -0.02, -179.95) # Without tool, in base NULLFRAME
pose_recup_loin = pose_recup.copy()
pose_recup_loin.z += 50

pose_devant_profilo = Pose(0, 300, 585, -168.03, 73.54, 102.41) # Without tool, in base NULLFRAME
pose_devant_profilo_loin = pose_devant_profilo.copy()
pose_devant_profilo_loin.y -= 50

pose_piece_conforme = Pose(400.86, 300.52, 430.88, 76.82, -0.02, -179.95) # Without tool, in base NULLFRAME
pose_piece_conforme_loin = pose_recup.copy()
pose_piece_conforme_loin.z += 50

pose_piece_non_conforme = Pose(-350, 400, 400, 49.19, -179, 0) # Without tool, in base NULLFRAME
pose_piece_non_conforme_loin = pose_recup.copy()
pose_piece_non_conforme_loin.z += 50

kuka_go_to_pose(new_home) # Home
kuka_go_to_pose(pose_devant_profilo_loin)
exit()
kuka_go_to_pose(pose_recup_loin) # Dessus tapis loin

kuka_go_to_pose(pose_recup) # Dessus tapis proche

send_kuka_3964R_single_char(GRAB) # Grab

kuka_go_to_pose(pose_recup_loin) # Dessus tapis loin

kuka_go_to_pose(new_home) # Back home
TRUE = True
while TRUE: # Les 4 premières faces
    kuka_go_to_pose(pose_devant_profilo_loin) # Approche du profilo
    # Il faut lancer le scan ici
    kuka_go_to_pose(pose_devant_profilo) # On passe devant le profilo pour scan
    # Stop scan
    kuka_go_to_pose(pose_devant_profilo_loin) # Départ du profilo
    
    # Rotation pour passer à la face suivante

# La dernière face (le dessous)


kuka_go_to_pose(new_home) # Home

# Le scan détermine si la pièce est conforme
piece_conforme = True

if piece_conforme:
    kuka_go_to_pose(pose_piece_conforme_loin) # Dessus tapis loin
    kuka_go_to_pose(pose_piece_conforme) # Dessus tapis proche
    send_kuka_3964R_single_char(DROP) # Drop
    kuka_go_to_pose(pose_piece_conforme_loin) # Dessus tapis loin
    kuka_go_to_pose(new_home) # Back home
else:
    kuka_go_to_pose(pose_piece_non_conforme_loin) # Dessus tapis loin
    kuka_go_to_pose(pose_piece_non_conforme) # Dessus tapis proche
    send_kuka_3964R_single_char(DROP) # Drop
    kuka_go_to_pose(pose_piece_non_conforme_loin) # Dessus tapis loin
    kuka_go_to_pose(new_home) # Back home

# for i in range(10):
#     p.y += 2
#     kuka_go_to_pose(p)
#     time.sleep(0.5)