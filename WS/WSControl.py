station_id = 0


class WSControl:
    def __init__(self, serial):
        global station_id
        self.serial = serial
        self.id = station_id
        station_id = station_id + 1

    def printPossibilites(self):
        print("Station #"+str(self.id)+" possible queries:")
