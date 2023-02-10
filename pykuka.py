import serial
s = serial.Serial(port="COM1", baudrate=9600, bytesize=8, parity=serial.PARITY_EVEN, stopbits=serial.STOPBITS_ONE)

# characters used to communicate
DLE = 16
STX = 2
ETX = 3
EOT = 4
DONE = 35   # '#' sent by the KUKA when it reaches the required location
GO = 71     # 'G' means 'GO'
HOME = 72   # 'H' means 'HOME'
POS = 80    # 'P' means current 'POSITION'
EXIT = 88   # 'X' means 'EXIT'
GRAB = 25
DROP = 27
SAISIE_BARRIERE = 21

class Pose:
    """Represents a pose (position x, y, z, and orientation a, b, c) of the robot."""
    def __init__(self, x, y, z, a, b, c):
        self.x = x
        self.y = y
        self.z = z
        self.a = a
        self.b = b
        self.c = c
    
    def __repr__(self):
        return f"X = {self.x}; Y = {self.y}; Z = {self.z}; A = {self.a}; B = {self.b}; C = {self.c}"

def calculate_bcc(input, init_value):
    """Calculate the BCC of a byte array to check for transmission errors."""
    res = init_value
    for i in input:
        res ^= i
    return res

def wait_for_kuka_3964R_data_buffer():
    """Read a string from the robot using the 3964R protocol."""
    len = 0
    s.read_until(bytes([STX]))
    s.write(bytes([DLE]))
    res = s.read_until(bytes([DLE, ETX]))[:-2]
    bcc = s.read()[0]
    s.write(bytes([DLE]))
    return res.decode('uft-8')

def get_pose_from_buffer(buffer):
    """Convert a string into a pose object."""
    s = buffer.split(' ')
    return Pose(float(s[0]), float(s[1]), float(s[2]), float(s[3]), float(s[4]), float(s[5]))

def build_buffer_from_pose(pose):
    """Convert a pose object into a string."""
    return f"{format(pose.x, '010.6f')} {format(pose.y, '010.6f')} {format(pose.z, '010.6f')} {format(pose.a, '010.6f')} {format(pose.b, '010.6f')} {format(pose.c, '010.6f')}"

def send_kuka_3964R_data_buffer(buffer):
    """Send a string to the robot using the 3964R protocol."""
    s.send(bytes([STX])) # send STX until we get DLE
    while(s.read()[0] != DLE):
        s.write(bytes([STX]))
    payload = bytes(buffer, 'utf-8') + bytes([DLE, ETX])
    bbc = calculate_bcc(payload, 0)
    s.send(payload + bytes([bbc]))
    s.read_until(bytes([DLE]))

def send_kuka_3964R_single_char(byte):
    """Send a single character to the robot using the 3964R protocol."""
    s.send(bytes([STX])) # send STX until we get DLE
    while(s.read()[0] != DLE):
        s.write(bytes([STX]))
    payload = bytes([byte, DLE, ETX])
    bbc = calculate_bcc(payload, 0)
    s.write(payload + bytes([bbc]))
    s.read_until(bytes([DLE]))

def send_kuka_3964R_single_double(double):
    """Send a double value to the robot using the 3964R protocol."""
    s.send(bytes([STX])) # send STX until we get DLE
    while(s.read()[0] != DLE):
        s.write(bytes([STX]))
    payload = bytes(format(double, '010.6f'), 'utf-8') + bytes([DLE, ETX])
    bbc = calculate_bcc(payload, 0)
    s.write(payload + bytes([bbc]))
    s.read_until(bytes([DLE]))

def kuka_go_to_pose(pose):
    """Ask the robot to reach a specific pose, return the pose that the robot actually reached"""
    send_kuka_3964R_single_char(GO)
    send_kuka_3964R_single_double(pose.x)
    send_kuka_3964R_single_double(pose.y)
    send_kuka_3964R_single_double(pose.z)
    send_kuka_3964R_single_double(pose.a)
    send_kuka_3964R_single_double(pose.b)
    send_kuka_3964R_single_double(pose.c)
    recv = wait_for_kuka_3964R_data_buffer()
    while recv[0] != chr(DONE):
        recv = wait_for_kuka_3964R_data_buffer()
    return get_pose_from_buffer(wait_for_kuka_3964R_data_buffer())