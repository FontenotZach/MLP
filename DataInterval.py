class DataInterval:
    intervalDuration = -1
    time = []
    p1 = []
    p2 = []
    p3 = []
    p4 = []
    p5 = []
    p6 = []
    p7 = []
    p8 = []
    aX = []
    aY = []
    aZ = []
    activity = -1   # 0 - cycling
                    # 1 - driving
                    # 2 - running
                    # 3 - sitting
                    # 4 - standing
                    # 5 - stair_up
                    # 6 - stair_down
                    # 7 - walking

    def __init__(self, duration, time, p1, p2, p3, p4, p5, p6, p7, p8, aX, aY, aZ, activity):
        self.intervalDuration = duration
        self.time = time
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.p4 = p4
        self.p5 = p5
        self.p6 = p6
        self.p7 = p7
        self.p8 = p8
        self.aX = aX
        self.aY = aY
        self.aZ = aZ
        self.activity = activity
