Profilométrie robotisée
=======================

Projet réalisé dans le cadre d'une UV projet à l'IMT Nord Europe qui consiste à scanner une pièce en 3D avec un robot Kuka et un profilomètre Keyence. Le but étant de détecter de potentielles imperfections sur des pièces imprimées en 3D.

A terme, tout doit passer par python : commande des mouvements du robot, démarrage des mesures et récupérations des données du profilomètre, assemblage des données et reconstitution d'un modèle 3D, détection des défauts, etc. Nous avons donc besoin de plusieurs briques de programme élémentaires, à commencer par des API de communication avec le robot et le profilomètre.

Table des matières
------------------

- [API Kuka](#api-kuka)
- [API Profilomètre](#api-profilomètre)

API Kuka
--------

Le robot Kuka reçoit les commandes envoyées depuis python grâce à une communication série. Côté robot, un programme KRL lit les données reçues sur le port série, les interprète, et effectue les mouvements demandés. Côté python, le fichier `pykuka.py` contient toutes les fonctions nécessaires à l'utilisateur pour envoyer des commandes au robot. Ce fichier pourra ensuite être importé dans le scipt principal.

La fonction `read_3964R_pose` est à utiliser lorsque la fonction `SEND` est appelée dans le programme du robot. Elle sert à récupérer et décoder la position renvoyée par le robot.
La fonction `send_3964R_single_char` est à utiliser lorsque la fonction `READ_CHAR` est appelée dans le programme du robot. Elle sert à envoyer un caractère au robot.
La fonction `send_3964R_single_double` est à utiliser lorsque la fonction `READ_DOUBLE` est appelée dans le programme du robot. Elle sert à envoyer un nombre décimal au robot.
La fonction `go_to_pose` est à utiliser uniquement si le programme `PC2KUKA`, qui permet d'interpréter des commandes de mouvement, tourne sur le robot. Elle sert à envoyer au robot l'ordre d'atteindre une position.
La fonction `get_pose` est à utiliser uniquement si le programme `PC2KUKA`, qui permet d'interpréter et de répondre à des commandes, tourne sur le robot. Elle sert à demander au robot d'envoyer sa position actuelle.

Ce fichier et ces fonctions peuvent être réutilisées dans d'autres projets utilisant un robot KUKA.

Utilisation du profilomètre
---------------------------

Voici quelques points importants pour comprendre le fonctionnement du profilomètre :

Le logiciel `LJ Navigator` permet de configurer le profilomètre, d'afficher et d'enregistrer des profils.
Un profil est une ligne prise par le laser du profilomètre. Sur ce modèle de profilomètre, une ligne fait 800 points. Chaque point correspond à une abscisse (x) et à une hauteur (z) mesurée par le profilomètre.
Un bouton `Démarrer affichage` permet d'afficher ce que le profilomètre voit. Le logiciel affiche alors la même chose que l'écran du profilomètre.
Un lot de profils (batch) est une suite de plusieurs profils individuels. La pièce se déplace devant le profilomètre lors de la prise des profils, transformant ainsi le nuage de point 2D d'un profil individuel à un nuage de points 3D (une coordonnée y vient donc s'ajouter). Le profilomètre dispose d'un mode batch qui réalise cette fonction.

Le profilomètre a deux modes principaux de fonctionnement :
- le mode normal qui permet de prendre des profils individuellements (voir la fonction `GetProfileAdvance` de la partie [API Profilomètre](#api-profilomètre)).
- le mode batch qui permet de faire des lots de profils. Ce mode nécéssite de choisir une fréquence d'échantillonage (fréquence à laquelle les différents profils du lot sont pris), un pas (distance entre les profils, qui dépend de la fréquence d'échantillonage et de la vitesse de la pièce sous le profilomètre) et un nombre maximal de profils à prendre. En mode batch, un enregistrement doit être déclenché (bouton `démarrer lot`, fonction `StartMeasure`), puis arrêté manuellement (bouton `arrêter lot`, fonction `StartMeasure`) ou automatiqument (lorsque le nombre de profils demandé est atteint). Attention, en mode batch, l'affichage n'est actif que pendant l'enregistrement, que ce soit sur l'écran du profilomètre ou sur le logiciel. Pendant l'enregistrement, des profils sont pris en lot, puis peuvent être enregistrés (fonction `GetBatchProfileAdvance`). Plusieurs modes d'acquisition sont possibles pour les lots :
    - le mode continu, qui prend des profils à intervalles réguliers avec une fréquence donnée, mais qui nécéssite d'avoir une vitesse de la pièce parfaitement connue pour la reconstituer proprement en 3D. C'est ce mode qui sera utilisé avec le robot.
    - le mode trigger, qui permet de déclencher la prise de chaque profil manuellement (fonction `Trigger`).
    - le mode codeur, qui permet de déclencher la prise de chaque prodil sur les changements du codeur incrémental externe qui peut être branché au profilomètre. Ceci est utile si c'est un axe linéaire muni d'un codeur qui fait bouger la pièce devant le profilomètre.

Tous ces paramètres (mode batch, fréquence, pas, nombre de profils) peuvent être régler grâce au bouton `réglage direct`.

API Profilomètre
----------------

La communication avec le profilomètre s'effectue grâce à au fichier `LJV7_IF.dll` fourni par Keyence. Ce type de DLL étant habituellement prévu pour être utilisé dans des langages bas niveau comme le C ou le C++, un fichier `pyprofilo.py` permettra de simplifier les appels aux fonctions du DLL en s'y interfaçant grâce au module `ctypes`. Ce dernier permet de travailler avec tous les types du langage C en python, de charger des fichiers DLL, et d'appeler les fonctions qui s'y trouvent, après un travail de convertion de types, de gestion de structures C, etc. Ce fichier pourra ensuite être importé dans le scipt principal.

Transformations 3D
------------------

Protocole de calibration
------------------------

Protocole en cas de changement de robot
---------------------------------------

Perspectives d'amélioration
---------------------------

Calibration automatique à base de déscente de gradient
- Système de calibration automatique (cf "base_point_cloud_dans_base_profilo = get_htm(0, 0, -170, 0, 0, 0)") afin de déterminer les 6 paramètres pour que les faces concordent parfaitement
- Réaliser le scan des 4 premières faces en une seule fois en faisant tourner le cube devant le profilo

TODO List
---------

faire un dossier avec les docs
faire un dosser avec les modèles 3d


pour calibrer facilement : projection orthogonale / commencer par les rotations et finir par les translations