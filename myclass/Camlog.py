import time


class Camlog():
    def __init__(self):
        now_time = time.time()
        self.phoneCount = 0
        self.startTime = now_time
        self.endTime = now_time
        self.concentTrateTime = 0
        self.happyCount = 0
        self.disgustedCount = 0

    def getData(self):
        return {
            "phoneCount": self.phoneCount,
            "happyCount": self.happyCount,
            "disgustedCount": self.disgustedCount
                }

    def concentrate(self):
        pass

    def phone(self):
        self.phoneCount += 1

    def notSeat(self):
        pass

    def happyCount(self):
        self.happyCount += 1

    def disgusted(self):
        self.disgustedCount += 1
