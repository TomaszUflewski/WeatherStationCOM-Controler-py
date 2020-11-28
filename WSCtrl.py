from COM import COM
from WS import WSControl

import time

def getInput(text=None, ws=None):
        if ws is not None:
            ws.printPossibilites()
            return input("Select query:")
        else:
            return input(text)


def printList(list):
    if len(list) == 0:
        return
    for i in range(0, len(list)):
        print(str(i)+": "+list[i].device)


def getTemp(respBytes):
    print(respBytes)
    return int.from_bytes(respBytes, byteorder="little", signed=True)


def getPressure(respBytes):
    value = int.from_bytes(resp, byteorder="little", signed=True)
    value = value/100  # move point
    return value/10  # form mb to kPa


def PLACEHOLDER(respBytes):
    pass


temp = getTemp
press = getPressure


def SwitchOnSensorName(name):
    return {
        "Temp": (getTemp, "C"),
        "Pressure": (getPressure, "kPa"),
        "Configuration and maintenace mode": (PLACEHOLDER, ".")
    }[name]


if __name__ == "__main__":
    ports = COM.GetPorts()
    printList(ports)
    target = int(getInput("Select COM:"))
    if target-1 > len(ports):
        print("No such port!")
        exit(-1)
    port = COM(ports[target].device)
    station = WSControl(port)

    station.comConnectToStation()

    while(True):
        op = getInput(ws=station)

        if op == "ctrl":
            station.startInteractiveMode()

        if op == "EOF":
            exit()

        bytesN = station.cmd(int(op))  # start data processing
        bytesOfResp = int.from_bytes(bytesN, byteorder='little')
        bytesOfResp = bytesOfResp & 3
        if bytesOfResp > 0:
            resp = bytearray()
            for i in range(0, bytesOfResp):
                resp[i:i] = station.getSerialOutput()
            sensorName = station.getSensorName(int(op))
            value = SwitchOnSensorName(sensorName)[0](resp)
            unit = SwitchOnSensorName(sensorName)[1]
            print(">>>> "+sensorName+" is : " + str(value) + unit)     
        print("--------------------------")
