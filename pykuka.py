import serial

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

s = serial.Serial(port="COM4", baudrate=9600, bytesize=8, parity=serial.PARITY_EVEN, stopbits=serial.STOPBITS_ONE)