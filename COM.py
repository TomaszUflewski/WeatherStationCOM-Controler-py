import serial.tools.list_ports
import serial


class COM:
    def __init__(self, id):
        self.com = serial.Serial(port=id)

    def printComName(self):
        print(self.com.name)

    def openPort(self):
        self.com.open()

    def closePort(self):
        self.com.close()

    def send(self, data):
        return self.write(data)

    def read(self, nBytes):
        return self.read(data)

    def setBAUD(self, BAUD_rate):
        self.com.baudrate = BAUD_rate

    def GetPorts():
        return list(serial.tools.list_ports.comports())
