import numpy as np
# Tool 0 Base 0
# x vers le sol
# y vers l'atelier
# z vers le tableau

x = -0.81
y = 501.10
z = 499.84
a = -169.5
b = 50.62
c = 95.50

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

def get_htm(x, y, z, a, b, c):
    #rotation_matrix = Rz(a) * Ry(b) * Rz(c)
    rotation_matrix = Rz(np.radians(a)) * Ry(np.radians(b)) * Rx(np.radians(c)) # this expression depends on the robot
    return np.vstack([np.hstack([rotation_matrix, np.array([[x], [y], [z]])]), np.array([[0, 0, 0, 1]])])

def apply_htm(htm: np.matrix, points: np.ndarray):
    transpose = np.matrix(points).T
    with_ones = np.vstack([transpose, np.ones(transpose.shape[1])])
    res = htm * with_ones
    return np.array(np.delete(res, 3, axis=0).T)

if __name__=="__main__":
    mat = get_htm(x, y, z, a, b, c)
    point_in_world = apply_htm(mat, np.array([0,10,100]))
    print(point_in_world)