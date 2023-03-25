import pykuka as kuka
import pykeyence as profilo
import transformations as tf
import os
import random as rd

DEVICE_ID           = 0
IP_ADDRESS          = "10.2.34.1"
PORT                = 24691
PROGRAM             = 8
VITESSE_ROBOT       = 0.0130 # m/s
FREQUENCE_PROFILO   = 100 # Hz
yStep = VITESSE_ROBOT * 1000 / FREQUENCE_PROFILO # mm
base_point_cloud_dans_base_profilo = tf.get_htm(0, 0, 0, 0, 0, 0) # la calibration étant effectuée correctement, ces deux bases sont confondues, et aucune translation ou rotation n'est à appliquer pour passer de l'une à l'autre.

profilo.Initialize(debug = True)
kuka.initialize("COM1")
profilo.GetVersion()
profilo.EthernetOpen(DEVICE_ID, IP_ADDRESS, PORT)

compteur_de_cube = 0

while True: # Pour chacun des cubes sur le convoyeur
    if input("Si cube à récupérer sur le convoyeur, appuyez sur 'Entrée'") == "stop": break
    kuka.send_3964R_single_char(kuka.GO)
    # Le Kuka part récupérer le cube
    kuka.send_3964R_single_char(kuka.GO) # Ce GO n'est écouté par le Kuka que quand il a récupéré le cube

    f = open(f"data/nuage{compteur_de_cube}.txt", 'w')
    f_brut = open("data/nuage_brut.txt", 'w')

    while True: # Pour scanner un cube
        # Start measure if Kuka at his "HOME" point
        go = kuka.read_3964R_single_char()
        if go != kuka.GO: break
        pose = kuka.read_3964R_pose() # Get starting point
        print(f"Position de départ : {pose}")
        profilo.StartMeasure(DEVICE_ID)
        done = kuka.read_3964R_single_char()
        profilo.StopMeasure(DEVICE_ID)

        point_cloud = profilo.GetBatchProfileAdvance(DEVICE_ID, 100, 1000, -yStep)

        base_outil_dans_base_profilo = tf.get_htm(pose.x, pose.y, pose.z, pose.a, pose.b, pose.c)
        base_profilo_dans_base_outil = base_outil_dans_base_profilo.I
        base_point_cloud_dans_base_outil = base_profilo_dans_base_outil * base_point_cloud_dans_base_profilo

        points_dans_base_outil = tf.apply_htm(base_point_cloud_dans_base_outil, point_cloud)

        f_brut.write(pose.to_string() + "\n")
        for i in range(len(point_cloud)):
            f.write(str(points_dans_base_outil[i][0]) + "\t" + str(points_dans_base_outil[i][1]) + "\t" + str(points_dans_base_outil[i][2]) + "\n")
            f_brut.write(str(point_cloud[i][0]) + "\t" + str(point_cloud[i][1]) + "\t" + str(point_cloud[i][2]) + "\n")
        f_brut.write("**********\n")

        # Batch treatment finished, send done to Kuka
        kuka.send_3964R_single_char(kuka.DONE)

    # EXIT received from Kuka

    f.close()
    f_brut.close()
    print(f"Le nuage de points a été écrit dans le fichier data/nuage{compteur_de_cube}.txt")

    piece_conforme = compteur_de_cube % 2 == 0 #rd.random() > 0.5 # A récupérer avec script de Robin et Arnaud
    print(f"La pièce est conforme : {piece_conforme}")
    if piece_conforme:
        kuka.send_3964R_single_char(kuka.YES)
    else:
        kuka.send_3964R_single_char(kuka.NO)

    compteur_de_cube += 1

profilo.CommClose(DEVICE_ID)
profilo.Finalize()
kuka.finalize()