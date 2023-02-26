import numpy as np

x = 1
y = 2
z = 3
a = np.radians(0.2)
b = 0.3
c = 0.4

t = np.matrix([[1, 0, 0, x],
               [0, 1, 0, y],
               [0, 0, 1, z],
               [0, 0, 0, 1]])

rx = np.matrix([[1, 0,         0,          0],
                [0, np.cos(a), -np.sin(a), 0],
                [0, np.sin(a), np.cos(a),  0],
                [0, 0,         0,          1]])

ry = np.matrix([[np.cos(b),  0, np.sin(b), 0],
                [0,          1, 0,         0],
                [-np.sin(b), 0, np.cos(b), 0],
                [0,          0, 0,         1]])

rz = np.matrix([[np.cos(c), -np.sin(c), 0, 0],
                [np.sin(c), np.cos(c),  0, 0],
                [0,         0,          1, 0],
                [0,         0,          0, 1]])

p = (np.matrix([0,0,0,1])).T
print(rx*ry*rz*t*p)
print(t*rx*ry*rz*p)
#print(T*Rz*Ry*Rx)