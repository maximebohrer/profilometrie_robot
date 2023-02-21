import os
import numpy as np
import csv
from pykeyence import *
import math

script_dir = os.path.dirname(__file__)
file_name_list = ["FaceFlat", "FaceUp"]

points = [[[]]]
def ceci_est_une_fonction():
    for file_name in file_name_list :
        file_path = os.path.join(script_dir, './Faces - Raw CSV/', file_name, '.csv')
        source_file = open(file_path, "r")
        file = list(csv.reader(source_file, delimiter = ";"))

        nb_lin = len(file)
        nb_col = len(file[0])
        print(f"Nombre de colonnes du scan : {nb_col}\nNombre de lignes scannées : {nb_lin}")

        file_np = np.asarray(file)
        file_np = np.char.replace(file_np, ",", ".")
        file_np = file_np.astype(np.float32)

        for i in range(nb_lin):
            for j in range(nb_col):
                x = i
                y = j
                z = file_np[i][j]

                points.append((x, y, z))

        # Distance capteur / objet : 200mm
        # Largeur du faisceau i.e. des nb_col colonnes : 62mm
        # Supprimer valeurs hors [-48 ; 48]

        

        # ind_min_file_np = np.unravel_index(np.argmin(file_np, axis=None), file_np.shape)
        # ind_max_file_np = np.unravel_index(np.argmax(file_np, axis=None), file_np.shape)
        # print(ind_min_file_np, ind_max_file_np)
        # print(file_np[ind_min_file_np], file_np[ind_max_file_np])


        '''
        file_path = os.path.join(script_dir, './Faces - TXT/test_a_supp4.txt')
        fichier_destination = open(file_path, 'w')
        cw = csv.writer(fichier_destination, delimiter='\t')
        '''

#############################################################################################
# Script principal
deviceID = 0
ipAddress = "10.2.34.1"
port = 24691
portHighSpeed = 24692


Initialize(debug = True)
GetVersion()
EthernetOpen(deviceID, ipAddress, port)
#a = GetProfileAdvance(deviceID, 800)
SetSetting_BatchMeasurement(deviceID, 8, SETTING_BATCH_MEASUREMENT_ON)
SetSetting_SamplingFrequency(deviceID, 8, SETTING_SAMPLING_FREQUENCY_200_HZ)
SetSetting_TriggerMode(deviceID, 8, SETTING_TRIGGER_MODE_CONTINUOUS)



exit()
GetMeasurementValue(deviceID)
Trigger(deviceID)
StartMeasure(deviceID)
StopMeasure(deviceID)

prof_complet_raw = GetBatchProfileAdvance(deviceID)
print("################ BATCH ################")
print(prof_complet_raw)

prof_raw = GetProfileAdvance(deviceID)
prof_clean = [a if a < 1000 else math.inf for a in prof_raw]

print("################ PAS BATCH ################")
print(prof_clean)

# print("\n".join(map(lambda x: str(x), prof_raw)))



# déclenchement  continu
# type : 10h
# Category : 00h
# item : 03h
# target 1~4 : 00h
# byte 0 : 1


input("Fin de la sim ? [ENTER]")
CommClose(deviceID)
Finalize()