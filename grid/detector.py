class Detector(object):
    def __init__(self, id: str, normal=(0, 0, -1), deadtime=0):
        self.id = id
        self.normal = normal
        self.deadtime = deadtime
