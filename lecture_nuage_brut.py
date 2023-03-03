import os
import numpy as np
from pykuka import Pose
import transformations as trans
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
from mpl_toolkits.mplot3d import Axes3D

f_brut = open("nuage_brut.txt", 'r')
f = open("data/nuage.txt", 'w')

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
        if i % 100 == 0:
            face.points.append([float(split[0]), float(split[1]), float(split[2])])
        i += 1
        line = f_brut.readline().strip()

    line = f_brut.readline().strip()

f.close()

def calcul_des_faces(faces, x, y, z, a, b, c):
    base_point_cloud_dans_base_profilo = trans.get_htm(x, y, z, a, b, c)
    cube = np.empty((0,3))
    for f in faces:
        base_outil_dans_base_profilo = trans.get_htm(f.x, f.y, f.z, f.a, f.b, f.c)
        base_profilo_dans_base_outil = base_outil_dans_base_profilo.I
        base_point_cloud_dans_base_outil = base_profilo_dans_base_outil * base_point_cloud_dans_base_profilo
        points_dans_base_outil = trans.apply_htm(base_point_cloud_dans_base_outil, f.points)
        cube = np.append(cube, points_dans_base_outil, axis=0)
    return cube

x_ini = -58
y_ini = -8.7
z_ini = -168.58
a_ini = -5.02
b_ini = -3.46
c_ini = 0.1
epsylon = 10

cube = calcul_des_faces(faces, x_ini, y_ini, z_ini, a_ini, b_ini, c_ini)

# fix, ax = plt.subplots()
# line, = ax.plot(cube, lw=2)
# ax.set_xlabel('Time [s]')

# créer une figure 3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# adjust the main plot to make room for the sliders
fig.subplots_adjust(bottom=0.25)

# ajouter des labels
ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')

# créer le nuage de points
graph = ax.scatter(cube[:, 0], cube[:, 1], cube[:, 2], marker='.', s=1)

# Make a horizontal slider to control x.
axis_x = fig.add_axes([0.25, 0.16, 0.65, 0.03])
x_slider = Slider(ax=axis_x,    label='x [mm]',   valmin=x_ini - epsylon, valmax=x_ini + epsylon,  valinit=x_ini)

# Make a horizontal slider to control y.
axis_y = fig.add_axes([0.25, 0.13, 0.65, 0.03])
y_slider = Slider(ax=axis_y,    label='y [mm]',   valmin=y_ini - epsylon, valmax=y_ini + epsylon,  valinit=y_ini)

# Make a horizontal slider to control z.
axis_z = fig.add_axes([0.25, 0.100, 0.65, 0.03])
z_slider = Slider(ax=axis_z,    label='z [mm]',   valmin=z_ini - epsylon, valmax=z_ini + epsylon,  valinit=z_ini)

# Make a horizontal slider to control a.
axis_a = fig.add_axes([0.25, 0.07, 0.65, 0.03])
a_slider = Slider(ax=axis_a,    label='a [°]',   valmin=a_ini - epsylon, valmax=a_ini + epsylon,  valinit=a_ini)

# Make a horizontal slider to control b.
axis_b = fig.add_axes([0.25, 0.04, 0.65, 0.03])
b_slider = Slider(ax=axis_b,    label='b [°]',   valmin=b_ini - epsylon, valmax=b_ini + epsylon,  valinit=b_ini)

# Make a horizontal slider to control c.
axis_c = fig.add_axes([0.25, 0.01, 0.65, 0.03])
c_slider = Slider(ax=axis_c,    label='c [°]',   valmin=c_ini - epsylon, valmax=c_ini + epsylon,  valinit=c_ini)

# The function to be called anytime a slider's value changes
def update(val):
    ax.clear()
    cube = calcul_des_faces(faces, x_slider.val, y_slider.val, z_slider.val, a_slider.val, b_slider.val, c_slider.val)
    ax.scatter(cube[:, 0], cube[:, 1], cube[:, 2], marker='.', s=1)
    fig.canvas.draw_idle()

# register the update function with each slider
x_slider.on_changed(update)
y_slider.on_changed(update)
z_slider.on_changed(update)
a_slider.on_changed(update)
b_slider.on_changed(update)
c_slider.on_changed(update)

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
button_augmenter_precision = Button(augmenter_precision, 'Up', hovercolor='0.975')

def upadate_los_cursores():
    global x_ini, y_ini, z_ini, a_ini, b_ini, c_ini
    global x_slider, y_slider, z_slider, a_slider, b_slider, c_slider
    global epsylon
    
    x_slider.val = x_ini
    x_slider.valinit = x_slider.val
    x_slider.valmin, x_slider.valmax = x_ini - epsylon, x_ini + epsylon
    x_slider.ax.set_xlim(x_slider.valmin, x_slider.valmax)
    x_slider.set_val(x_ini)

    y_slider.val = y_ini
    y_slider.valinit = y_slider.val
    y_slider.valmin, y_slider.valmax = y_ini - epsylon, y_ini + epsylon
    y_slider.ax.set_xlim(y_slider.valmin, y_slider.valmax)
    y_slider.set_val(y_ini)

    z_slider.val = z_ini
    z_slider.valinit = z_slider.val
    z_slider.valmin, z_slider.valmax = z_ini - epsylon, z_ini + epsylon
    z_slider.ax.set_xlim(z_slider.valmin, z_slider.valmax)
    z_slider.set_val(z_ini)

    a_slider.val = a_ini
    a_slider.valinit = a_slider.val
    a_slider.valmin, a_slider.valmax = a_ini - epsylon, a_ini + epsylon
    a_slider.ax.set_xlim(a_slider.valmin, a_slider.valmax)
    a_slider.set_val(a_ini)

    b_slider.val = b_ini
    b_slider.valinit = b_slider.val
    b_slider.valmin, b_slider.valmax = b_ini - epsylon, b_ini + epsylon
    b_slider.ax.set_xlim(b_slider.valmin, b_slider.valmax)
    b_slider.set_val(b_ini)

    c_slider.val = c_ini
    c_slider.valinit = c_slider.val
    c_slider.valmin, c_slider.valmax = c_ini - epsylon, c_ini + epsylon
    c_slider.ax.set_xlim(c_slider.valmin, c_slider.valmax)
    c_slider.set_val(c_ini)
    
def f_augmenter_precision(event):
    f_sauvegarder_valeurs("")
    global epsylon
    if epsylon > 1 :    epsylon -= 1
    else :              print("[f_augmenter_precision] Précision maximale déjà atteinte")
    upadate_los_cursores()

button_augmenter_precision.on_clicked(f_augmenter_precision)

# Create a `matplotlib.widgets.Button` to reset the sliders to initial values.
diminuer_precision = fig.add_axes([0.8, 0.28, 0.1, 0.04])
button_diminuer_precision = Button(diminuer_precision, 'Down', hovercolor='0.975')

def f_diminuer_precision(event):
    f_sauvegarder_valeurs("")
    global epsylon
    epsylon += 1
    upadate_los_cursores()

button_diminuer_precision.on_clicked(f_diminuer_precision)

# Create a `matplotlib.widgets.Button` to reset the sliders to initial values.
sauvegarder_valeurs = fig.add_axes([0.8, 0.32, 0.1, 0.04])
button_sauvegarder_valeurs = Button(sauvegarder_valeurs, 'Save', hovercolor='0.975')

def f_sauvegarder_valeurs(event):
    global x_ini, y_ini, z_ini, a_ini, b_ini, c_ini
    x_ini, y_ini, z_ini, a_ini, b_ini, c_ini = x_slider.val, y_slider.val, z_slider.val, a_slider.val, b_slider.val, c_slider.val

button_sauvegarder_valeurs.on_clicked(f_sauvegarder_valeurs)

plt.show()