import numpy as np

x = 1
y = 2
z = 3
a = np.radians(0.2)
b = 0.3
c = 0.4

#a sur z
#c sur x
#b sur y

def Rx(a):
    return np.matrix([[1, 0,         0         ],        
                      [0, np.cos(a), -np.sin(a)],
                      [0, np.sin(a), np.cos(a) ]])

def Ry(a):
    return np.matrix([[np.cos(a),  0, np.sin(a)],
                      [0,          1, 0        ],        
                      [-np.sin(a), 0, np.cos(a)]])

def Rz(a):
    return np.matrix([[np.cos(a), -np.sin(a), 0],
                      [np.sin(a), np.cos(a),  0],
                      [0,         0,          1]])

def get_homogeneous_transformation_matrix(x, y, z, a, b, c):
    rotation_matrix = Rz(a) * Ry(b) * Rz(c)
    return np.vstack([np.hstack([rotation_matrix, np.array([[x], [y], [z]])]), np.array([[0, 0, 0, 1]])])