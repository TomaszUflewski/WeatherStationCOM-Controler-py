from COM import COM
from serial import SerialException as SerialE

from WS import WSControl


def getInput(text=None, ws=None):
        if ws is not None:
            ws.printPossibilites()
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
    print("Opening: "+ports[target].device)
    port = COM(ports[target].device)
    try:
        port.openPort()
    except SerialE as e:
        print("Error occured when opening " + ports[target].device + ": "+str(e))
        # exit(-1)
    except:
        print("Fatal error occured when opening - exit now!")
        exit(-1)
    print("Port is now open!")

    station = WSControl(port)
    getInput(ws=station)
