from COM import COM
from WS import WSControl
from WS import DataInterpreter as DI


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

    op = getInput(ws=station)
    bytesN = station.cmd(int(op))  # start data processing
    bytesOfResp = int.from_bytes(bytesN, byteorder='little')
    bytesOfResp = bytesOfResp & 3
    resp = bytearray()
    for i in range(0, bytesOfResp):
        resp[i:i] = station.getSerialOutput()
    temp = int.from_bytes(resp, byteorder="little", signed=True)
    print("Temp is : " + str(temp))
