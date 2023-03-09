Etapes principales du TP

MODE EXPERT
Se mettre en mode expert (Configurer / Groupe utilisateur) mot de passe : kuka

DÉFINITION BASE PROFILOMÈTRE
1/ Placer la pince 20cm sous le profilomètre (cf. photo) Attention position centre pince
2/ Configurer outil "pince" n°3 et base "profilometre" n°3 (Configurer / "Outil / Base actuels")
3/ Relever la position actuelle de la pince (Visualiser / Position actuelle / Cartésien) (uniquement x,y ,z)
4/ Reporter cette position comme position de la base profilomètre (Service / Mesurer / Base / Entrée numérique)
5/ Vérifier que les coordonnées de la pince sont désormais à 0, 0, 0

RÉCUPÉRATION CUBE SUR CONVOYEUR (base WORLD)
Il faut maintenant aller chercher un cube à la position du cube jaune sur le convoyeur. On va devoir utiliser les mouvements PTP pour aller vite et les LIN pour s'approcher précisément du cube situé sur le convoyeur.
1/ Se placer 50mm au dessus du cube (déplacement PTP) (point recup_cube)
2/ Descendre sur le cube (déplacement LIN)
3/ Actionner la pince
4/ Remonter en position recup_cube (déplacement LIN)

CHANGEMENT DE PRISE DU CUBE
Le cube a été pris par sa face supérieure, face que nous voulons aussi scanner. Il faut donc le poser couché sur la table afin de le récupérer par son pied.

Kuka va en position prêt pour faire scan (base profilomètre obligatoire)

SCAN DE 5 FACES DU CUBE (base profilomètre)


Code :
1/ [P] Faire les initialisations et envoyer GO
2/ [K] Reçoit le GO, fait ce qui précède et envoie GO puis sa position
3/ [P] Start measure, [K] LIN_REL
4/ [K] Quand a fini, envoie DONE
5/ [P] Récupère le profile avec le profilo, renvoie GO quand a fini, [K] renvoie GO quand est revenu en position initiale et a tourné de 90° pour prochain scan
6/ On recommence

On va affiner les coordonnées de la base profilomètre.
Une fois les scans finis, on obtient
- nuage.txt (que des points, assez imprécis pour l'instant)
- nuage_brut.txt (ligne 1 position initiale du robot puis les points récupérés puis "**************" etc.)
On lance calibration_assistant.py et on précise les x, y, z, a, b et c de la base profilomètre. On affine ensuite ces valeurs pour que les points collent.
On modifie alors la base profilomètre avec ces nouvelles valeurs.

LA BASE EST MAINTENANT CALIBRÉE PILE POIL COMME IL FAUT

On refait un scan et on s'intéresse à nuage.txt
On va chercher à connaître les dimensions extérieures du cube grâce au script de Robin et Arnaud

La fin de ce script renvoie un booléen :
    True -> pièce conforme, renvoie sur tapis position cube bleu
    False -> pièce défectueuse, dépôt sur table position cube gris