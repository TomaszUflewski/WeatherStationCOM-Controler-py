from enum import Enum, unique

station_id = 0


@unique
class OperationState(Enum):
    NORMAL_OPERATION = 0
    OPERATION_MAINTENACE = 1


VERSION_SENSORS = {
    1: [("Temp", bytes.fromhex('01'))],

    2: [("Temp", bytes.fromhex('01')),
        ("Pressure", bytes.fromhex('03')),
        ("Configuration and maintenace mode", bytes.fromhex('0F'))],
}


class WSControl:

    class ConfigurationMaintenace:
        __SELECTIONS = [
            ("UART-TEST", bytes.fromhex('01'))
        ]

        def __init__(self):
            pass

        def getCode(self, id):
            return self.__SELECTIONS[id][1]

        def printPossibilites(self):
            print("possible operations:")
            for i in range(0, len(self.__SELECTIONS)):
                print(str(i)+": " + self.__SELECTIONS[i][0])

        def run(self, op):
            pass

    def __init__(self, serial):
        global station_id
        self.serial = serial
        self.id = station_id
        station_id = station_id + 1
        self.__version = False
        self.__mode = OperationState.NORMAL_OPERATION
        self.__ConfaMain = WSControl.ConfigurationMaintenace()

    def startInteractiveMode(self):
        c = ""
        while True:
            c = input("#")
            if c == "stop":
                exit()
            elif c == "n":
                print(self.serial.read())
                continue
            op = bytes.fromhex(c)
            self.serial.send(op)
            print(self.serial.read())

    def comConnectToStation(self):
            self.serial.send(bytes.fromhex('3C'))
            handshake = self.serial.read()
            if handshake != bytes.fromhex('C3'):
                print("No handshake! " + str(handshake))
                exit(-1)
            print("Handshake OK!")
            if self.__version is False:
                self.__getFirmwareVersion()

    def __getFirmwareVersion(self):
        self.serial.send(bytes.fromhex('FF'))  # query for version
        version = self.serial.read()
        # don't care about byteorder
        version = int.from_bytes(version, byteorder='big')
        self.__version = version

    def printPossibilites(self):
        print("Station #"+str(self.id) + " v."+str(self.__version)+" possible queries:")
        sensors = VERSION_SENSORS[self.__version]
        for i in range(0, len(sensors)):
            print(str(i)+": "+sensors[i][0])

    def __buildQuery(self, sensor):
        header = bytes.fromhex('C0')
        hT = int.from_bytes(header, byteorder='little')
        op = hT + int.from_bytes(sensor, byteorder='little')
        return bytes([op])

    def getSensorName(self, op):
        sensors = VERSION_SENSORS[self.__version]
        return sensors[op][0]

    def cmd(self, op):
        sensors = VERSION_SENSORS[self.__version]

        if sensors[op][1] == bytes.fromhex('0F'):
            self.__mode = OperationState.OPERATION_MAINTENACE
        else:
            self.__mode = OperationState.NORMAL_OPERATION

        if self.__mode == OperationState.OPERATION_MAINTENACE:
            selected = sensors[op][1]
            query = self.__buildQuery(selected)
            self.serial.send(query)
            self.__ConfaMain.printPossibilites()
            sel = input("#: ")
            selected = self.__ConfaMain.getCode(int(sel))
        else:
            selected = sensors[op][1]
        query = self.__buildQuery(selected)  # in bytes
        self.serial.send(query)
        return self.serial.read()

    def getSerialOutput(self):
        return self.serial.read()
