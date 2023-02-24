import os
import numpy as np
import csv
from pykeyence import *
import math
import time

SCRIPT_DIR = os.path.dirname(__file__)
FILE_NAMES_LIST = ["FaceFlat", "FaceUp"]

points = [[[]]]
def ceci_est_une_fonction():
    for file_name in FILE_NAMES_LIST :
        file_path = os.path.join(SCRIPT_DIR, './Faces - Raw CSV/', file_name, '.csv')
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
DEVICE_ID = 0
IP_ADDRESS = "10.2.34.1"
PORT = 24691
PROGRAM = 8

prof_raw =[]

Initialize(debug = False)
GetVersion()
EthernetOpen(DEVICE_ID, IP_ADDRESS, PORT)

debut = time.time()
while time.time() - debut < 1:
    lin_raw = GetProfileAdvance(DEVICE_ID)
    prof_raw.append(lin_raw)

nb_lin = len(prof_raw)
nb_col = len(prof_raw[0])

prof_clean = prof_raw.copy()
for i in range(nb_lin):
    for j in range(nb_col):
        if prof_clean[i][j] > 21000: 
            prof_clean[i][j] = math.inf

print(prof_clean)
#############################################################################################
exit()
# Adieu monde cruel

# Set up
SetSetting_BatchMeasurement(DEVICE_ID, PROGRAM, SETTING_BATCH_MEASUREMENT_OFF)
SetSetting_SamplingFrequency(DEVICE_ID, PROGRAM, SETTING_SAMPLING_FREQUENCY_200_HZ)
SetSetting_TriggerMode(DEVICE_ID, PROGRAM, SETTING_TRIGGER_MODE_CONTINUOUS)

GetMeasurementValue(DEVICE_ID)
Trigger(DEVICE_ID)

StartMeasure(DEVICE_ID)
StopMeasure(DEVICE_ID)

prof_complet_raw = GetBatchProfileAdvance(DEVICE_ID) # MARCHE PAS

input("Fin de la sim ? [ENTER]")
CommClose(DEVICE_ID)
Finalize()