
# sudo chmod 666 /dev/ttyUSB0
# roslaunch faze4_moveit demo.launch rviz_tutorial:=true


# import rospy 
# from std_msgs.msg import String
# from sensor_msgs.msg import JointState

from abc import abstractmethod
import serial, time
import serial.tools.list_ports

import sys
sys.path.append('/home/znkzjs/bot/python')
from singleton import Singleton

from enum import Enum
#TODO: add mqtt
# from mqtt_helper import  g_mqtt

class HARD_ROBOT_ONLINE_LEVEL(Enum):
    OFF_LINE = 1
    ONLINE_AS_REPRAP = 2
    ONLINE_AS_SOWER = 3
    HOMED = 4

class ReprapArm(metaclass=Singleton):
    '''
    Can communacate with reprap_arm,  for example:  Marlin
    Send gcode to serial, confirm Reprap got the gcode correctly.
    '''
    def __init__(self):
        '''
        This will create an object, But will not connect to Marlin
        '''
        self.is_connected = False
        self.__serialport = serial.Serial()
        self.__counter = 0
        self.__echo_is_on = False 

        self.state = HARD_ROBOT_ONLINE_LEVEL.OFF_LINE

    def try_to_find_ports(self, portname, do_list_ports = False):
        myports = [tuple(p) for p in list(serial.tools.list_ports.comports())]
        found_com_port = False

        for a,b,c in myports:
            if do_list_ports:
                print(a)
                print(b)
                print(c)
            if a == portname:
                found_com_port = True
        return found_com_port

    def connect_reprap_controller(self, portname, baudrate):
        self.__serialport.port = portname
        self.__serialport.baudrate  = baudrate
        self.__serialport.timeout = 1
        self.__serialport.writeTimeout = 2

        if self.try_to_find_ports(portname):
            self.__serialport.open()
            if self.__echo_is_on:
                print ('Reprap_host::Serial port is opened.')
            while True:
                xx = self.__serialport.readline()
                mm = bytes.decode(xx)
                if (mm == ''):
                    self.is_connected = True
                    return True
        else:
            # Can not find 'dev/ttyUSB0'
            print('Can not find %s ' %portname)
            return False
        self.state = HARD_ROBOT_ONLINE_LEVEL.ONLINE_AS_REPRAP

    def set_echo_on(self, is_on):
        self.__echo_is_on = is_on

    def __send_gcode_mcode(self, raw_gcode):
        '''
        raw_gcode is a pure string, not include formated 
        '''
        self.__counter += 1
        self.__serialport.write(str.encode(raw_gcode +'\r\n'))
        if self.__echo_is_on:
            print ('>>> %s' % raw_gcode)
        got_ok = False
        while not got_ok:
            response_a = self.__serialport.readline()
            response = bytes.decode(response_a)
            if(response == 'ok\n'):
                got_ok = True
                if self.__echo_is_on:
                    print ('OK')
            elif (response ==''):
                time.sleep(0.1)
            elif self.__echo_is_on:
                print("<<< " + response)
    @abstractmethod
    def set_joints_angle_in_degree(self, IK_dict):
        print('set_joints_angle_in_degree not implatemented')

    def set_fan_speed(self, speed):
        '''
        speed from 0 to 255
        '''
        self.__send_gcode_mcode('M106 S' + str(speed))

    def disable_motor_sleep(self):
        self.__send_gcode_mcode('M84 S0')  #Disable sleep

    def print_homing_sensor_states(self):
        '''
        print out status of all joints home sensor.
        include joint5? I forgot it, depend on Marlin firmware. 
        '''
        self.__send_gcode_mcode('M84')
        while True:
            self.set_echo_on(True)
            self.__send_gcode_mcode('M119')
            # rospy.sleep(1)
            time.sleep(1)

    def allow_cold_extrusion(self):
        self.__send_gcode_mcode('M302 S0') # Allow extrusion at any temperature
    
    def wait_for_movement_finsished(self):
        self.__send_gcode_mcode('M400')

    def home(self, home_x=False, home_y=False, home_z=False):
        if home_x:
            self.__send_gcode_mcode('G28 X')
        if home_y:
            self.__send_gcode_mcode('G28 Y')
        if home_z:
            self.__send_gcode_mcode('G28 Z')

    def move_to_xyz(self, x, y, z=None, speed_mm_per_min=None):
        gcode = 'G1'
        if x is not None:
            gcode += 'X' + str(x)
        if y is not None:
            gcode += 'Y' + str(y)
        if z is not None:
            gcode += 'Z' + str(z)
        if speed_mm_per_min is not None:
            gcode += 'F' + str(speed_mm_per_min)
        self.__send_gcode_mcode(gcode)

    def bridge_send_gcode_mcode(self, the_code):
        self.__send_gcode_mcode(the_code)

    @abstractmethod
    def home_all_joints(self):
        print('[Warning] This is an abstract method')
        
    
class TestArm(ReprapArm):
    pass

if __name__ == "__main__":
    test = TestArm()
    test.set_echo_on(True)
    test.connect_reprap_controller('/dev/ttyUSB0', 115200)
    test.bridge_send_gcode_mcode('M114')
    test.home(home_y=True)

