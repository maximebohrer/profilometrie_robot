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
    
    @classmethod
    def from_string(cls, string):
        """Build a pose object from a string. The string must consist of 6 double values separated by spaces."""
        s = string.split(' ')
        return cls(float(s[0]), float(s[1]), float(s[2]), float(s[3]), float(s[4]), float(s[5]))
    
    def to_string(self):
        """Convert the pose object into a string. 6 doubles values separated by spaces are returned."""
        return f"{format(self.x, '010.6f')} {format(self.y, '010.6f')} {format(self.z, '010.6f')} {format(self.a, '010.6f')} {format(self.b, '010.6f')} {format(self.c, '010.6f')}"
    
    def __repr__(self):
        return f"X = {self.x}; Y = {self.y}; Z = {self.z}; A = {self.a}; B = {self.b}; C = {self.c}"

def calculate_bcc(input, init_value):
    """Calculate the BCC of a byte array to check for transmission errors."""
    bcc = init_value
    for i in input:
        bcc ^= i
    return bcc

def read_kuka_3964R_data_buffer():
    """Read a byte buffer from the robot using the 3964R protocol. Block until the buffer is received."""
    s.read_until(bytes([STX]))                    # wait for STX
    s.write(bytes([DLE]))                         # then send DLE
    payload = s.read_until(bytes([DLE, ETX]))     # read the payload until DLE ETX
    bcc = s.read()[0]                             # read the BCC
    s.write(bytes([DLE]))                         # write DLE
    if bcc != calculate_bcc(payload, 0):
        raise Exception("Transmission error")     # throw error if received BCC does not match calculated BCC
    return payload[:-2]                           # strip DLE and ETX and return the payload

def read_kuka_3964R_string():
    """Read a buffer from the robot using the 3964R protocol, and convert it to a string. Block until the string is received."""
    return read_kuka_3964R_data_buffer().decode('utf-8')

def read_kuka_3964R_pose():
    """Read a buffer from the robot using the 3964R protocol, and convert it to a pose. Block until the pose is received. The conversion is done by the from_string method of the Pose class: the buffer must consist of six double values separated by spaces."""
    return Pose.from_string(read_kuka_3964R_data_buffer().decode('utf-8'))

def send_kuka_3964R_data_buffer(bytes):
    """Send a byte buffer to the robot using the 3964R protocol."""
    s.send(bytes([STX]))                          # send STX until we get DLE
    while(s.read()[0] != DLE):
        s.write(bytes([STX]))
    payload = bytes + bytes([DLE, ETX])           # add BLE ETX to the payload
    bbc = calculate_bcc(payload, 0)               # calculate BCC to be added to the payload
    s.send(payload + bytes([bbc]))                # send payload DLE ETX BCC
    s.read_until(bytes([DLE]))                    # wait for DLE

def send_kuka_3964R_string(string):
    """Send a string to the robot using the 3964R protocol. The string is converted to a byte buffer and is then sent."""
    send_kuka_3964R_data_buffer(bytes(string, 'utf-8'))

def send_kuka_3964R_single_char(byte):
    """Send a single character to the robot using the 3964R protocol. """
    send_kuka_3964R_data_buffer(bytes([byte]))

def send_kuka_3964R_single_double(double):
    """Send a double value to the robot using the 3964R protocol. The value is sent as a string (000.000000)."""
    send_kuka_3964R_data_buffer(bytes(format(double, '010.6f'), 'utf-8'))

def kuka_go_to_pose(pose):
    """Ask the robot to reach a specific pose, return the pose that the robot actually reached"""
    send_kuka_3964R_single_char(GO)               # send GO signal
    send_kuka_3964R_single_double(pose.x)         # send the 6 double values the robot is waiting for
    send_kuka_3964R_single_double(pose.y)
    send_kuka_3964R_single_double(pose.z)
    send_kuka_3964R_single_double(pose.a)
    send_kuka_3964R_single_double(pose.b)
    send_kuka_3964R_single_double(pose.c)
    recv = read_kuka_3964R_data_buffer()
    while recv[0] != DONE:                        # wait DONE signal
        recv = read_kuka_3964R_data_buffer()
    return read_kuka_3964R_pose()                 # read and return pose

if __name__ == '__main__':
    send_kuka_3964R_single_char(POS)              # send POS signal to request position
    p = read_kuka_3964R_pose()                    # read position
    for i in range(10):
        p.y += 2
        kuka_go_to_pose(p)