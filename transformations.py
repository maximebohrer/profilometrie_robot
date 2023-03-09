import numpy as np
# Tool 0 Base 0
# x vers le sol
# y vers l'atelier
# z vers le tableau
#a sur z
#c sur x
#b sur y

def Rx(a: float):
    """Calculate the rotation matrix around the x axis. a is the angle in radians."""
    return np.matrix([[1, 0,         0         ],
                      [0, np.cos(a), -np.sin(a)],
                      [0, np.sin(a), np.cos(a) ]])

def Ry(a: float):
    """Calculate the rotation matrix around the y axis. a is the angle in radians."""
    return np.matrix([[np.cos(a),  0, np.sin(a)],
                      [0,          1, 0        ],
                      [-np.sin(a), 0, np.cos(a)]])

def Rz(a: float):
    """Calculate the rotation matrix around the z axis. a is the angle in radians."""
    return np.matrix([[np.cos(a), -np.sin(a), 0],
                      [np.sin(a), np.cos(a),  0],
                      [0,         0,          1]])

def get_htm(x: float, y: float, z: float, a: float, b: float, c: float) -> np.matrix:
    """Get the homogeneous transformation matrix from the x, y, z, a, b, c of the robot. x, y and z are in mm; a, b and c in degrees. It is used to go from tool coordinates to base coordinates for example.
    The matrix can then be inverted (using the .I method) to represent the reverse transformation (base coordinates to tool coordinates for example), or multiplied together to chain transmormations.
    When multiplying matrices together, the last matrix of the product is the first transformation that is applied."""
    a, b, c = np.radians(a), np.radians(b), np.radians(c)
    rotation_matrix = Rz(a) * Ry(b) * Rx(c)                              # this expression depends on the robot (alpha = a, beta = b, gamma = c)
    return np.vstack([np.hstack([rotation_matrix, np.array([[x], [y], [z]])]), np.array([[0, 0, 0, 1]])])    # construction of the homogeneous transformation matrix

def apply_htm(htm: np.matrix, points: np.ndarray) -> np.ndarray:
    """Apply the homogeneous transformation matrix to a list of points.
    This function is used to handle the array manipulations, since a fourth coordinate (1) needs to be added to a 3D point before multiplying it by a homogeneous transformation matrix."""
    transpose = np.matrix(points).T                                    # transpose the array so that the points are columns
    with_ones = np.vstack([transpose, np.ones(transpose.shape[1])])    # adding a row of ones for the next calculation
    res = htm * with_ones                                              # applying the homogeneous transformation matrix to the list of points
    return np.array(np.delete(res, 3, axis=0).T)                       # remove the last row and transpose again

if __name__=="__main__":
    x = -131.86
    y = 517.30
    z = 599.15
    a = -136.66
    b = 23.74
    c = 67.92
    tool_in_world = get_htm(x, y, z, a, b, c)
    point_in_world = apply_htm(tool_in_world, np.array([-37.17,-40.58,66.03]))
    print(point_in_world)