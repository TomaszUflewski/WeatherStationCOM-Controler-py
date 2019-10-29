import serial.tools.list_ports
import serial
from serial import SerialException as SerialE


class COM:
    def __init__(self, id):
        self.com = serial.Serial(port=id, timeout=3)

    def printComName(self):
        print(self.com.name)

    def openPort(self):
        try:
            self.com.open()
        except SerialE as e:
            print("Error occured when opening " + self.com.port + ": "+str(e))
            exit(-1)
        except:
            print("Fatal error occured when opening "+self.com.port+" - exit now!")
            exit(-1)

    def closePort(self):
        self.com.close()

    def send(self, data):
        return self.com.write(data)

    def read(self, nBytes=1):
        return self.com.read(nBytes)

    def setBAUD(self, BAUD_rate):
        self.com.baudrate = BAUD_rate

    def GetPorts():
        return list(serial.tools.list_ports.comports())
