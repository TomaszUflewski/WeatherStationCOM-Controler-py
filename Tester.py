import serial

s = serial.Serial("COM5", timeout=3)


def read():
    return s.read(1)


def x(h):
    return bytes.fromhex(h)


def send(d):
    s.write(x(d))


def state():
    send('fa')
    print(read())


def cReq():
    send('aa')
    print(read())
