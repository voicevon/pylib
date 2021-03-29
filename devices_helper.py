import serial.tools.list_ports

class DevicesHelper():
    def __init__(self):
        pass

    def serial_port_from_chip_name(self, chip_name):
        myports = [tuple(p) for p in list(serial.tools.list_ports.comports())]
        for port_name,chip,detail in myports:
            if chip == chip_name:
                return port_name

    def serial_port_from_location(self, location):
        myports = [tuple(p) for p in list(serial.tools.list_ports.comports())]
        for port_name,chip,detail in myports:
            xx =  detail[-7:]
            # print(xx)
            if xx == location:
                return port_name

    def serial_port_list_all(self):
        myports = [tuple(p) for p in list(serial.tools.list_ports.comports())]
        for port_name,chip,detail in myports:
            print('-------------------------------------')
            print(port_name)
            print(chip)
            print(detail)

   

    
if __name__ == "__main__":
    helper = DevicesHelper()
    helper.serial_port_list_all()
    portname = helper.serial_port_from_location('1-2.4.1')
    print(portname)
    portname = helper.serial_port_from_location('1-2.4.4')
    print(portname)


