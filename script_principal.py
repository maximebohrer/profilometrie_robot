import time
from pykuka import *
from pykeyence import *

depart = Pose(0, 0, -10)
arrivee = Pose(0, 100, -10)

go_to_pose(depart)
go_to_pose(arrivee)
