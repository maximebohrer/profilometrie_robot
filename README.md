Profilométrie robotisée
=======================

Projet réalisé dans le cadre d'une UV projet à l'IMT Nord Europe qui consiste à scanner une pièce en 3D avec un robot Kuka et un profilomètre Keyence. Le but étant de détecter de potentielles imperfections sur des pièces imprimées en 3D.

A terme, tout doit passer par python : commande des mouvements du robot, démarrage des mesures et récupérations des données du profilomètre, assemblage des données et reconstitution d'un modèle 3D, détection des défauts, etc. Nous avons donc besoin de plusieurs briques de programme élémentaires, à commencer par des API de communication avec le robot et le profilomètre.

Table des matières
------------------

- [API Kuka](#api-kuka)
- [Utilisation du profilomètre](#utilisation-du-profilomètre)
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


Configuration du profilomètre
-----------------------------

Pour configurer le profilomètre Keyence LJ-V7080, on utilise le logiciel `LJ Navigator`. Voici les différentes étapes pour configurer correctement le profilomètre :
- Connectez le profilomètre à l'ordinateur via un câble USB et allumez le profilomètre.
- Ouvrez `LJ Navigator`.
- Dans la fenêtre `Liste de périphériques`, vérifiez que le profilomètre est bien détecté. Si le profilomètre n'apparaît pas, vérifiez la connexion internet ou réinstallez les drivers du profilomètre.
- Cliquez sur le bouton `Connexion` pour se connecter au profilomètre. Si la connexion échoue, vérifiez que le profilomètre est bien allumé et qu'il est connecté au même réseau.
- Dans la fenêtre `Réglage rapide`, vérifiez que les paramètres de base sont corrects (par exemple la vitesse de déplacement du profilomètre). Ces paramètres peuvent être modifiés en cliquant sur le bouton `Réglage direct`.



Dans la fenêtre `Réglage déclench.`, réglez les paramètres de mesure du profilomètre. Les paramètres sont les suivants :
- `Mode de déclenchement :` Choix du mode de mesure (Voir partie [Utilisation du profilomètre](#utilisation-du-profilomètre))
- `Fréquence d'échantillonnage :` c'est la fréquence à laquelle les mesures sont effectuées. Plus cette fréquence est élevée, plus la mesure sera précise mais plus le temps de mesure sera long. La fréquence d'échantillonnage doit être choisie en fonction de la précision désirée et du temps de mesure acceptable.
- `Pas de mesure :` Cela correspond à la distance réelle entre deux points de mesure consécutifs, utilisée pour mettre à l'échelle le nuage de points 3D obtenu. Ce paramètre doit être déterminé avec précision pour garantir la précision de la reconstruction 3D de la pièce.
- `Nombre de points de mesure :` c'est le nombre de points de mesure qui seront pris. Plus ce nombre est élevé, plus la mesure sera précise mais plus le temps de mesure sera long. Le nombre de points de mesure doit être choisi en fonction de la précision désirée et du temps de mesure acceptable.

Dans la fenêtre `Réglage image.`, réglez les paramètres d'image du profilomètre. Les paramètres sont les suivants :
- `Mode de réflexion` : Permet d'ajuster les paramètres du laser du profilomètre de sorte à mieux mesurer les refiefs. 
- `Optimiser réglages` : Le logiciel détermine une succession de réglages possibles afin d'améliore le rendu de l'image. 
- Enfin, on peut accéder à d'avantages de réglages en cliquant sur `Aller au regl. avancé`. On y trouve des paramètres de `plage de mesure :` c'est la plage de mesure en hauteur et en largeur que le profilomètre peut mesurer. Elle doit être choisie en fonction de la hauteur des pièces à mesurer.

On trouve finalement des options permettant d'appliquer des `filtres de traitement` dans l'onglet `Profil`, mais nous ne l'utilisons pas.

Dans la fenêtre `Mesure`, cliquez sur le bouton `Démarrer affichage` pour afficher les mesures en temps réel. Les mesures seront affichées sur l'écran du profilomètre et dans la fenêtre `Affichage` de `LJ Navigator`.

- Cliquez sur le bouton `Démarrer lot` pour commencer la mesure en mode lot. Les mesures seront prises en continu jusqu'à ce que le nombre de points de mesure soit atteint ou que l'utilisateur arrête la mesure manuellement en cliquant sur le bouton `Arrêter lot`.

- Une fois la mesure terminée, les données peuvent être enregistrées en cliquant sur le bouton `Enregistrer`. Les données peuvent être enregistrées dans différents formats, notamment `CSV, TXT, DAT, BMP, JPEG, TIFF`

API Profilomètre
----------------

La communication avec le profilomètre s'effectue grâce à au fichier `LJV7_IF.dll` fourni par Keyence. Ce type de DLL étant habituellement prévu pour être utilisé dans des langages bas niveau comme le C ou le C++, un fichier `pyprofilo.py` permettra de simplifier les appels aux fonctions du DLL en s'y interfaçant grâce au module `ctypes`. Ce dernier permet de travailler avec tous les types du langage C en python, de charger des fichiers DLL, et d'appeler les fonctions qui s'y trouvent, après un travail de convertion de types, de gestion de structures C, etc. Ce fichier pourra ensuite être importé dans le scipt principal.

Transformations 3D
------------------

Le fichier `transformations.py` contient des fonctions permettant de faire des changements de base en robotique. Des matrices de transformations homogènes sont utilisées.

La fonction `get_htm` permet de calculer une matrice de transformation homogène à partir à partir de 6 paramètres x, y, z, a, b, c qui représentent la position et l'orientation d'une base B dans une base A. Cette matrice permettra ensuite de convertir des points dont les coordonnées sont exprimées dans la base B aux mêmes points dont les coordonnées sont exprimées dans la base A. Cette fonction utilise des matrices `numpy`, qui peuvent être multipliées entres elles et inversées. Inverser une matrice permet de passer de la base A à B au lieu de passer de la base B à A. Multiplier des matrices entres elles permet d'enchainer les changements de base. La dernière matrice du produit correspond au premier changement de base.

La fonction `apply_htm` prend en argument une matrice de transformation homogène et une liste de points, et applique la transformation. Les points ne peuvent en effet pas être multipliés directement à la matrice, il faut lui ajouter une 4ème coordonnée, et les exprimer sous forme de matrice colonne. Cette fonction se charge de ceci. Les points doivent être passés à la fonction sous la forme d'un tableau `numpy` de la forme [[x, y, z], [x, y, z], ...].

Attention : les paramètres de rotation a, b, et c ne signifient pas toujours la même chose pour les différents modèles de robot. Pour que le projet fonctionne, il faut être sûr du calcul de la matrice de rotation. Par exemple, pour le robot utilisé, la matrice de rotation est `rotation_matrix = Rz(a) * Ry(b) * Rx(c)`, c'est-à-dire qu'un point est décrit par une rotation autour de x d'angle c, puis autour de y d'angle b, puis autour de z d'angle a, puis par la translation x, y, z. D'autres conventions existent cependant, comme la convention ZYZ (`rotation_matrix = Rz(a) * Ry(b) * Rz(c)`). Cette expression, qui se trouve dans la fonction `get_htm`, est donc à modifier en fonction du robot utilisé, et à déterminer à partir de sa documentation ou en faisant différents essais. Pour savoir si la matrice est correcte, suivre ce protocole :
- Créer une nouvelle base dans le robot avec une position et une orientation aléatoire.
- Relever les paramètres x, y, z, a, b, c de cette base, et les utiliser pour créer une matrice de transformation homogène avec `get_htm`. Cette matrice permettra donc de passer des coordonnées de cette base aux coordonnées de la base world du robot.
- Emmener l'outil à une position et une orientation aléatoire.
- Affichier sur le robot et relever les coordonnées x, y, z de ce point dans la base nouvellement créée, et les exprimer dans la base world grâce à la fonction `apply_htm`.
- Afficher sur le robot les coordonnées de ce même point, mais dans la base world (base principale, base 0) et comparer avec les résultats obtenus. Si tout correspond, alors la matrice de rotation est juste. Sinon, en tester une autre.

Protocole de calibration
------------------------

La reconstitution du scan 3D à partir des différents profils repose sur le fait que la base "profilometre" du robot soit parfaitement alignée avec la base du nuage de points renvoyé par le profilomètre. En effet, si les points renvoyés par le profilomètre peuvent être considérés comme étant dans la base "profilometre" du robot (ce qui est le cas si les deux bases sont parfaitement alignées), alors un changement de base peut permettre d'exprimer ces points dans le repère de l'outil. La pièce scannée étant fixe dans le repère de l'outil, passer tous les profils dans la base de l'outil permet automatiquement de reconstituer la pièce. Ces changements de bases sont fait en Python grâce aux coordonnées (de l'outil pince dans le repère profilometre) renvoyés par le robot avant chaque profil.

Le repère du nuage de points renvoyé par le profilomètre est représenté dans cette image :


Protocole en cas de changement de robot
---------------------------------------

Pour continuer d'utiliser le projet avec un robot différent, deux étapes sont nécéssaire :
- S'assurer que la matrice de rotation soit calculée correctement, ou modifier cette dernière. Pour cela, suivre le protocole décrit dans la partie [Transformations 3D](#transformations-3d).
- Effectuer une calibration du système en suivant le protocole de la partie [Protocole de calibration](#protocole-de-calibration)

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