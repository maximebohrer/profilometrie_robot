"""
+------------------------------------------------------------------------+
|                         IMT Nord Europe - 2023                         |
|   BOHRER Maxime, LENTREBECQ Maxime, RUSHENAS Arnaud, TRAMAILLE Robin   |
+------------------------------------------------------------------------+

Assistant de calibration
"""

import numpy as np
from pykuka import Pose
import transformations as tf
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
from mpl_toolkits.mplot3d import Axes3D

f_brut = open("data/nuage_brut.txt", 'r')

class Face:
    def __init__(self, x, y, z, a, b, c, points):
        self.x, self.y, self.z, self.a, self.b, self.c = x, y, z, a, b, c # Pose de départ
        self.points = points

faces = []

line = f_brut.readline().strip()
while line != "":
    i = 0
    pose = Pose.from_string(line)
    face = Face(pose.x, pose.y, pose.z, pose.a, pose.b, pose.c, [])
    faces.append(face)
    line = f_brut.readline().strip()
    while line != "**********":
        split = line.split("\t")
        if i % 300 == 0:
            face.points.append([float(split[0]), float(split[1]), float(split[2])])
        i += 1
        line = f_brut.readline().strip()
    line = f_brut.readline().strip()

print("Entrez ci-dessous la position et l'orientation actuelles de la base \"profilometre\" du robot, c'est-à-dire lorsque le dernier scan a été effectué. Le but est ensuite de faire varier ces paramètres pour déplacer la base \"profilometre\" sur l'origine du nuage de points du profilomètre, afin que les positions renvoyées par le robot donnent lieu à des changements de base corrects. Une simulation 3D permet de visualiser l'effet que le changement aurait sur le nuage de points. Une fois que le scan est proprement reconstitué, les nouveaux paramètres de base peuvent être entrés dans le robot.")
x_ini = float(input("X actuel de la base \"profilometre\" : "))
y_ini = float(input("Y actuel de la base \"profilometre\" : "))
z_ini = float(input("Z actuel de la base \"profilometre\" : "))
a_ini = float(input("A actuel de la base \"profilometre\" : "))
b_ini = float(input("B actuel de la base \"profilometre\" : "))
c_ini = float(input("C actuel de la base \"profilometre\" : "))

ancienne_base_profilo_dans_monde = tf.get_htm(x_ini, y_ini, z_ini, a_ini, b_ini, c_ini) # base actuelle enregistrée dans le robot, c'est-à-dire celle avec laquelle les points ont été enregistrés
monde_dans_ancienne_base_profilo = ancienne_base_profilo_dans_monde.I

epsylon = 10

# créer une figure 3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_proj_type('ortho')

# adjust the main plot to make room for the sliders
fig.subplots_adjust(bottom=0.25)

# ajouter des labels
ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')

def draw_graph(x, y, z, a, b, c):
    # calculate cube
    nouvelle_base_profilo_dans_monde = tf.get_htm(x, y, z, a, b, c) # nouvelle base profilo, c'est à dire la base du nuage de points, que l'on essaye de trouver
    base_point_cloud_dans_ancienne_base_profilo = monde_dans_ancienne_base_profilo * nouvelle_base_profilo_dans_monde # correction artificielle des points pour l'affichage
    for f in faces:
        base_outil_dans_base_profilo = tf.get_htm(f.x, f.y, f.z, f.a, f.b, f.c)
        base_profilo_dans_base_outil = base_outil_dans_base_profilo.I
        base_point_cloud_dans_base_outil = base_profilo_dans_base_outil * base_point_cloud_dans_ancienne_base_profilo
        f.points_dans_base_outil = tf.apply_htm(base_point_cloud_dans_base_outil, f.points)

    # draw cube
    colors = ["red", "green", "blue", "darkorange", "purple", "darkcyan"]
    ax.clear()
    for i, f in enumerate(faces):
        if i < 4: ax.scatter(f.points_dans_base_outil[:, 0], f.points_dans_base_outil[:, 1], f.points_dans_base_outil[:, 2], marker='.', s=4, c=colors[i % len(colors)])
    ax.set_box_aspect(list(map(lambda lim3d: lim3d[1] - lim3d[0], [ax.get_xlim3d(), ax.get_ylim3d(), ax.get_zlim3d()])))
    fig.canvas.draw_idle()

draw_graph(x_ini, y_ini, z_ini, a_ini, b_ini, c_ini)

axis_x = fig.add_axes([0.25, 0.16, 0.65, 0.03])
axis_y = fig.add_axes([0.25, 0.13, 0.65, 0.03])
axis_z = fig.add_axes([0.25, 0.10, 0.65, 0.03])
axis_a = fig.add_axes([0.25, 0.07, 0.65, 0.03])
axis_b = fig.add_axes([0.25, 0.04, 0.65, 0.03])
axis_c = fig.add_axes([0.25, 0.01, 0.65, 0.03])

def create_sliders():
    global x_slider, y_slider, z_slider, a_slider, b_slider, c_slider

    axis_x.clear()
    axis_y.clear()
    axis_z.clear()
    axis_a.clear()
    axis_b.clear()
    axis_c.clear()

    x_slider = Slider(ax=axis_x,    label='x [mm]',   valmin=x_ini - epsylon,   valmax=x_ini + epsylon,   valinit=x_ini)
    y_slider = Slider(ax=axis_y,    label='y [mm]',   valmin=y_ini - epsylon,   valmax=y_ini + epsylon,   valinit=y_ini)
    z_slider = Slider(ax=axis_z,    label='z [mm]',   valmin=z_ini - epsylon,   valmax=z_ini + epsylon,   valinit=z_ini)
    a_slider = Slider(ax=axis_a,    label='a [°]',    valmin=a_ini - epsylon,   valmax=a_ini + epsylon,   valinit=a_ini)
    b_slider = Slider(ax=axis_b,    label='b [°]',    valmin=b_ini - epsylon,   valmax=b_ini + epsylon,   valinit=b_ini)
    c_slider = Slider(ax=axis_c,    label='c [°]',    valmin=c_ini - epsylon,   valmax=c_ini + epsylon,   valinit=c_ini)

    x_slider.on_changed(update)
    y_slider.on_changed(update)
    z_slider.on_changed(update)
    a_slider.on_changed(update)
    b_slider.on_changed(update)
    c_slider.on_changed(update)

# The function to be called anytime a slider's value changes
def update(val):
    draw_graph(x_slider.val, y_slider.val, z_slider.val, a_slider.val, b_slider.val, c_slider.val)

create_sliders()

# Create a button to reset the sliders to initial values.
resetax = fig.add_axes([0.8, 0.20, 0.1, 0.04])
button_reset = Button(resetax, 'Reset', hovercolor='0.975')

def f_reset(event):
    x_slider.reset()
    y_slider.reset()
    z_slider.reset()
    a_slider.reset()
    b_slider.reset()
    c_slider.reset()

button_reset.on_clicked(f_reset)

# Create a button to increase the precision reset the sliders to initial values.
augmenter_precision = fig.add_axes([0.8, 0.24, 0.1, 0.04])
button_augmenter_precision = Button(augmenter_precision, 'Augmenter précision', hovercolor='0.975')
    
def f_augmenter_precision(event):
    global epsylon
    global x_ini, y_ini, z_ini, a_ini, b_ini, c_ini
    x_ini, y_ini, z_ini, a_ini, b_ini, c_ini = x_slider.val, y_slider.val, z_slider.val, a_slider.val, b_slider.val, c_slider.val
    epsylon /= 2
    create_sliders()

button_augmenter_precision.on_clicked(f_augmenter_precision)

# Create a `matplotlib.widgets.Button` to reset the sliders to initial values.
diminuer_precision = fig.add_axes([0.8, 0.28, 0.1, 0.04])
button_diminuer_precision = Button(diminuer_precision, 'Diminuer précision', hovercolor='0.975')

def f_diminuer_precision(event):
    global epsylon
    global x_ini, y_ini, z_ini, a_ini, b_ini, c_ini
    x_ini, y_ini, z_ini, a_ini, b_ini, c_ini = x_slider.val, y_slider.val, z_slider.val, a_slider.val, b_slider.val, c_slider.val
    epsylon *= 2
    create_sliders()

button_diminuer_precision.on_clicked(f_diminuer_precision)

# Create a `matplotlib.widgets.Button` to reset the sliders to initial values.
sauvegarder_valeurs = fig.add_axes([0.8, 0.32, 0.1, 0.04])
button_sauvegarder_valeurs = Button(sauvegarder_valeurs, 'Sauver', hovercolor='0.975')

def f_sauvegarder_valeurs(event):
    global x_ini, y_ini, z_ini, a_ini, b_ini, c_ini
    x_ini, y_ini, z_ini, a_ini, b_ini, c_ini = x_slider.val, y_slider.val, z_slider.val, a_slider.val, b_slider.val, c_slider.val
    create_sliders()

    with open("data/nuage_pour_les_gars.txt", 'w') as f:
        for face in faces:
            for point in face.points_dans_base_outil:
                f.write(f"{point[0]}\t{point[1]}\t{point[2]}\n")

button_sauvegarder_valeurs.on_clicked(f_sauvegarder_valeurs)

plt.show()

print("Voici les nouvelles valeurs des paramètres de la base \"profilometre\" à entrer dans le robot :")
print(f"X = {x_slider.val}; Y = {y_slider.val}, Z = {z_slider.val}, A = {a_slider.val}, B = {b_slider.val}, C = {c_slider.val}")
#f_sauvegarder_valeurs(0)