import time
from pykuka import *
from pykeyence import *

# Des positions
pose_recup = Pose(355.53, 304.83, 454.93, 0, 1.95, 178.7) # Without tool, in base NULLFRAME
pose_recup_loin = pose_recup.copy()
pose_recup_loin.z += 50

pose_devant_profilo = Pose(-307, 466, 630, 141.75, 1.84, -177) # Without tool, in base NULLFRAME
pose_devant_profilo_loin = pose_devant_profilo.copy()
pose_devant_profilo_loin.y -= 130

pose_dessous_profilo = Pose(0, 300, 585, -168.03, 73.54, 102.41) # Without tool, in base NULLFRAME
pose_dessous_profilo_loin = pose_dessous_profilo.copy()
pose_dessous_profilo_loin.y -= 70

pose_piece_conforme = pose_recup.copy()
pose_piece_conforme.y += 100
pose_piece_conforme_loin = pose_piece_conforme.copy()
pose_piece_conforme_loin.z += 50

pose_piece_non_conforme = Pose(-350, 400, 400, 49.19, -179, 0) # Without tool, in base NULLFRAME
pose_piece_non_conforme_loin = pose_piece_non_conforme.copy()
pose_piece_non_conforme_loin.z += 50

#####################################################

print(read_3964R_pose())







exit()


send_3964R_single_char(HOME)

# Récupération de la pièce
go_to_pose(pose_recup_loin, PTP) # Dessus tapis loin
go_to_pose(pose_recup, PTP) # Dessus tapis proche
send_3964R_single_char(GRAB) # Grab
go_to_pose(pose_recup_loin, PTP) # Dessus tapis loin

for i in range(4): # Les 4 premières faces
    go_to_pose(pose_devant_profilo_loin, PTP) # Approche du profilo
    # Il faut lancer le scan ici
    go_to_pose(pose_devant_profilo, PTP) # On passe devant le profilo pour scan
    # Stop scan
    go_to_pose(pose_devant_profilo_loin, PTP) # Départ du profilo
    
    # Rotation pour passer à la face suivante
    pose_devant_profilo.b += 90
    pose_devant_profilo_loin.b += 90
    break

# La dernière face (le dessous)
go_to_pose(pose_dessous_profilo_loin, PTP) # Approche du profilo
# Il faut lancer le scan ici
go_to_pose(pose_dessous_profilo, LIN_SLOW) # On passe sous le profilo pour scan
# Stop scan
go_to_pose(pose_dessous_profilo_loin, PTP)

send_3964R_single_char(HOME) # Home

# Le scan détermine si la pièce est conforme
piece_conforme = False

if piece_conforme:
    go_to_pose(pose_piece_conforme_loin) # Dessus tapis loin
    go_to_pose(pose_piece_conforme) # Dessus tapis proche
    send_3964R_single_char(DROP) # Drop
    go_to_pose(pose_piece_conforme_loin) # Dessus tapis loin
    send_3964R_single_char(HOME) # Back home
else:
    go_to_pose(pose_piece_non_conforme_loin) # Dessus tapis loin
    go_to_pose(pose_piece_non_conforme) # Dessus tapis proche
    send_3964R_single_char(DROP) # Drop
    go_to_pose(pose_piece_non_conforme_loin) # Dessus tapis loin
    send_3964R_single_char(HOME) # Back home

send_3964R_single_char(EXIT)