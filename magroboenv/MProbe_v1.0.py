import math
import random
import numpy as np
import win32com.client  # Python ActiveX Client
import logging

##########global class and function definition#############
VI_PATH='C:\\LabView\\Mark2\\Python_Comm\\Python_Comm.vi'

def square(x):
    return x*x

#class representing the coordinates
class Coordinate():
    MAX_VAL = 250.0
    MIN_VAL = -250.0

    MAX_DEVIATE = 5.0
    
    def __init__(self):
        self.x=0.0
        self.y=0.0
        self.z=0.0
        
    def set_coordinate(self, Coordinate):
        self.x=Coordinate.x
        self.y=Coordinate.y
        self.z=Coordinate.z
        
    def set_xyz(self, x, y, z):
        self.x=x
        self.y=y
        self.z=z
        
    def set_x(self, x):
        self.x=x
        
    def set_y(self, y):
        self.y=y

    def set_z(self, z):
        self.z=z
     
    def __str__(self):
        return "({}, {}, {})".format(self.x, self.y, self.z)

    def find_distance(self, Coordinate):
        sum = square(self.x - Coordinate.x) + square(self.y - Coordinate.y) + square(self.z - Coordinate.z)
        return math.sqrt(sum)

    def set_random_xyz(self):
        self.x = random.uniform(Coordinate.MAX_VAL, Coordinate.MIN_VAL)
        self.y = random.uniform(Coordinate.MAX_VAL, Coordinate.MIN_VAL)
        self.z = random.uniform(Coordinate.MAX_VAL, Coordinate.MIN_VAL)
        xyz = [ self.x, self.y, self.z ]
        return xyz

    def set_random_dev_xyz(self, Coordinate):
        self.x = random.uniform(Coordinate.x - Coordinate.MAX_DEVIATE, Coordinate.x + Coordinate.MAX_DEVIATE)
        self.y = random.uniform(Coordinate.y - Coordinate.MAX_DEVIATE, Coordinate.y + Coordinate.MAX_DEVIATE)
        self.z = random.uniform(Coordinate.z - Coordinate.MAX_DEVIATE, Coordinate.z + Coordinate.MAX_DEVIATE)
        xyz = [ self.x, self.y, self.z ]
        return xyz
        
#class representing the coordinates
class MagneticMoment():

    MAX_MM = 7.0
    MIN_MM = -7.0
    
    def __init__(self):
        self.mx=0.0
        self.my=0.0
        self.mz=0.0
        
    def set_mmoment(self, MagneticMoment):
        self.mx=MagneticMoment.mx
        self.my=MagneticMoment.my
        self.mz=MagneticMoment.mz
        
    def set_xyz(self, x, y, z):
        self.mx=x
        self.my=y
        self.mz=z
        
    def set_mx(self, x):
        self.mx=x
        
    def set_my(self, y):
        self.my=y

    def set_mz(self, z):
        self.mz=z
     
    def __str__(self):
        return "({}, {}, {})".format(self.mx, self.my, self.mz)

#Electric Current class
class Current():
    MAX_CURRENT = 4.0
    MIN_CURRENT = -4.0
    MAX_DEVIATE = 0.01
    MIN_DEVIATE = -0.01
    
    ac_low = np.array([MIN_CURRENT, MIN_CURRENT, MIN_CURRENT, MIN_CURRENT, MIN_CURRENT, MIN_CURRENT, MIN_CURRENT, MIN_CURRENT, MIN_CURRENT])
    ac_high = np.array([MAX_CURRENT, MAX_CURRENT, MAX_CURRENT, MAX_CURRENT, MAX_CURRENT, MAX_CURRENT, MAX_CURRENT, MAX_CURRENT, MAX_CURRENT])
    
    def __init__(self, name='unknown'):
        self.amp = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        self.amp_label = ('a_1','a_2','a_3','a_4','a_5','a_6','a_7','a_8','a_9')
        self.name = name
		
    def __str__(self):
        return "({}, {})".format(self.name, self.amp)

    def uniform_current(self, curr):
        while True:
            dev = random.uniform(Current.MAX_DEVIATE, Current.MIN_DEVIATE)
            dev = curr + dev
            if dev < Current.MAX_CURRENT and dev > Current.MIN_CURRENT:
                return dev
            
    def generate_random(self):
        for i in range(9):
            #self.amp[i] = self.uniform_current(self.amp[i])
            self.amp[i] = random.uniform(Current.MAX_CURRENT, Current.MIN_CURRENT)
        #print("random:{}".format(self))
	
    def set_current(self, a1, a2, a3, a4, a5, a6, a7, a8, a9):
        self.amp[0] = a1
        self.amp[1] = a2
        self.amp[2] = a3
        self.amp[3] = a4
        self.amp[4] = a5
        self.amp[5] = a6
        self.amp[6] = a7
        self.amp[7] = a8
        self.amp[8] = a9
        #print(self)

    def set_sys_current(self, index, cur):
        if cur < Current.MAX_CURRENT and cur > Current.MIN_CURRENT:
            self.amp[index] = cur
            VI.setcontrolvalue(self.amp_label[index], str(self.amp[index]))

    def set_all_sys_current(self, cur):
        for i in range(9):
            self.amp[i] = cur[i]
            VI.setcontrolvalue(self.amp_label[i], str(self.amp[i]))

    def read_sys_current(self):
        pass

        
    def get_a1(self):
        return self.amp[0]

    def get_a2(self):
        return self.amp[1]

    def get_a3(self):
        return self.amp[2]
    
    def get_a4(self):
        return self.amp[3]

    def get_a5(self):
        return self.amp[4]

    def get_a6(self):
        return self.amp[5]

    def get_a7(self):
        return self.amp[6]

    def get_a8(self):
        return self.amp[7]

    def get_a9(self):
        return self.amp[8]

#class representing the probing robot 
class MProbe():
    
    master_label = ('master_x', 'master_y', 'master_z', 'master_mx', 'master_my', 'master_mz')
    slave_label = ('slave_x', 'slave_y', 'slave_z', 'slave_mx', 'slave_my', 'slave_mz')

    ob_low  = np.array([Coordinate.MIN_VAL, Coordinate.MIN_VAL, Coordinate.MIN_VAL, MagneticMoment.MIN_MM, MagneticMoment.MIN_MM, MagneticMoment.MIN_MM])
    ob_high = np.array([Coordinate.MAX_VAL, Coordinate.MAX_VAL, Coordinate.MAX_VAL, MagneticMoment.MAX_MM, MagneticMoment.MAX_MM, MagneticMoment.MAX_MM])
    
    def __init__(self, name='unknown'):
        self.coordinate = Coordinate()
        self.last_coordinate = Coordinate()
        self.last_coordinate_dist = 0.0
        self.mmoment = MagneticMoment()
        self.last_mmoment = MagneticMoment()
        self.velocity = 0.0
        self.name = name

    def __str__(self):
        return "({}, {}, {})".format(self.name, self.coordinate, self.mmoment)

    def set_coordinate(self, Coordinate):
        self.last_coordinate.set_coordinate(self.coordinate)
        self.coordinate.set_coordinate(Coordinate)
        self.last_coordinate_dist = self.coordinate.find_distance(self.last_coordinate)

    def set_x(self, x):
        self.last_coordinate.set_x(self.coordinate.x)
        self.coordinate.set_x(float(x))
        self.last_coordinate_dist = self.coordinate.find_distance(self.last_coordinate)
        print(self)

    def set_y(self, y):
        self.last_coordinate.set_y(self.coordinate.y)
        self.coordinate.set_y(float(y))
        self.last_coordinate_dist = self.coordinate.find_distance(self.last_coordinate)
        print(self)

    def set_z(self, z):
        self.last_coordinate.set_z(self.coordinate.z)
        self.coordinate.set_z(float(z))
        self.last_coordinate_dist = self.coordinate.find_distance(self.last_coordinate)
        print(self)

    def set_orientation(self, x, y, z, mx, my, mz):
        self.last_mmoment.set_mmoment(self.mmoment)
        self.mmoment.set_xyz(mx, my,mz)
        self.last_coordinate.set_coordinate(self.coordinate)
        self.coordinate.set_xyz(x, y, z)
        self.last_coordinate_dist = self.coordinate.find_distance(self.last_coordinate)
        #print(self)
        logging.debug(self)
        
    def read_sys_orientation(self):
        ori = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        
        if self.name == 'Slave':
            for i in range(6):
                ori[i] = VI.getcontrolvalue(MProbe.slave_label[i])
            
        elif self.name == 'Master':
            for i in range(6):
                ori[i] = VI.getcontrolvalue(MProbe.master_label[i])

        self.set_orientation(ori[0], ori[1], ori[2], ori[3], ori[4], ori[5])

        return ori

        
    def set_random_xyz(self):
        xyz = self.coordinate.set_random_xyz()
        print("Target: {}".format(self))
        logging.debug("Target: {}".format(self))
        return xyz
    
    def set_random_dev_xyz(self, MProbe):
        xyz = self.coordinate.set_random_dev_xyz(MProbe.coordinate)
        print("Target: {}".format(self))
        logging.debug("Target: {}".format(self))
        return xyz        
        
    def find_distance(self, MProbe):
        dist = self.coordinate.find_distance(MProbe.coordinate)
        return dist

#create a labview client
LabVIEW = win32com.client.Dispatch("Labview.Application")
VI = LabVIEW.getvireference(VI_PATH)
master=MProbe('Master')
slave=MProbe('Slave')
goal=MProbe('Goal')
read_current=Current('reading')
desired_current=Current('desired')

