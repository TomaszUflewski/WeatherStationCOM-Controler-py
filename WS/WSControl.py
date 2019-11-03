station_id = 0


VERSION_SENSORS = {
    1: [("Temp", bytes.fromhex('01'))],
}


class WSControl:
    def __init__(self, serial):
        global station_id
        self.serial = serial
        self.id = station_id
        station_id = station_id + 1
        self.__version = False

    def comConnectToStation(self):
            self.serial.send(bytes.fromhex('3C'))
            handshake = self.serial.read()
            if handshake != bytes.fromhex('C3'):
                print("No handshake! " + str(handshake))
                exit(-1)
            print("Handshake OK!")

    def __getFirmwareVersion(self):
        self.serial.send(bytes.fromhex('FF'))  # query for version
        version = self.serial.read()
        # don't care about byteorder
        version = int.from_bytes(version, byteorder='big')
        self.__version = version

    def printPossibilites(self):
        if self.__version is False:
            self.__getFirmwareVersion()
        print("Station #"+str(self.id)+" possible queries:")
        sensors = VERSION_SENSORS[self.__version]
        for i in range(0, len(sensors)):
            print(str(i)+": "+sensors[i][0])

    def __buildQuery(self, sensor):
        header = bytes.fromhex('C0')
        hT = int.from_bytes(header, byteorder='little')
        op = hT + int.from_bytes(sensor, byteorder='little')
        return bytes([op])

    def cmd(self, op):
        sensors = VERSION_SENSORS[self.__version]
        selected = sensors[op][1]
        query = self.__buildQuery(selected)  # in bytes
        self.serial.send(query)
        return self.serial.read()

    def getSerialOutput(self):
        return self.serial.read()
