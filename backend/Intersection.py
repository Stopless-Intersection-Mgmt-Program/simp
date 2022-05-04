import math

class Intersection:
    def __init__(self, algorithm):
        self.algorithm = algorithm
        self.size = 40 # length (m) of one side of the intersection
        self.time = 0 # clock to track time (s) elapsed
        self.cars = [] # list of cars monitored by the intersection


    def schedule(self, car):
        # adds car for intersection to handle
        # based on scheduling algorithm, should assign a car to follow

        # TEMPORARY CODE FOR TESTING
        car.time = self.time # synchronize clocks
        if len(self.cars) > 0:
            for fcar in reversed(self.cars):
                if self.follow(car, fcar): break
        self.cars.append(car)

        return # to be implemented


    def follow(self, car1, car2):
        # sets car1 to pass through intersection immediately after car2
        # if car1 and car2 do not share a critical section, do nothing

        # TEMPORARY CODE FOR TESTING
        overlap = self.overlap(car1.path, car2.path, 0)
        if overlap == None: return False
        goal = car2.timeTo(overlap[1])
        fastest, slowest = car1.rangeTo(overlap[0])
        if goal < fastest: car1.setCourse(overlap[0], fastest)
        if goal <= slowest: car1.setCourse(overlap[0], goal)
        if goal > slowest: print("Houston, we got a problem...")
        return True

        return # to be implemented


    def overlap(self, path1, path2, buffer):
        # returns start distance on path1 and end distance on path2 of critical section
        (li1, lo1), (li2, lo2) = path1, path2
        turn1, turn2 = (lo1 - li1) % 8 // 2, (lo2 - li2) % 8 // 2
        reld = (li2 - li1) % 8 // 2 # relative direction of other car

        if reld == 0: # path1 is path2
            if turn1 // 2 == turn2 // 2: return 0, 8 # if paths have same starting lane
            else: return None # if not in same lane, no critical section

        if reld == 1: # path2 is left of path1
            lcritical = [[None, None, (0, 0.5), (0.5, 1)], # U turn
                        [(0.6, 0.7), (0.5, 0.5), (0, 0.7), None], # left turn
                        [None, None, (0.1, 0.9), None], # straight
                        [None, None, (0.3, 1), None]] # right turn
            cs = lcritical[turn1][turn2]

        if reld == 2: # path2 is opposite of path1
            ocritical = [[None, None, (0.6, 1), None], # U turn
                        [None, None, (0.6, 0.5), None], # left turn
                        [(0.4, 0.8), (0.7, 1), None, None], # straight
                        [None, None, None, None]] # right turn
            cs = ocritical[turn1][turn2]

        if reld == 3: # path2 is right of path1
            rcritical = [[None, (0.3, 0.9), None, None], # U turn
                        [None, (0.2, 0.7), None, None], # left turn
                        [(0.2, 0.9), (0.5, 0.3), (0.6, 0.3), (0.7, 1)], # straight
                        [(0.3, 1), None, None, None]] # right turn
            cs = rcritical[turn1][turn2]
        if cs == None: return None

        # adjust for intersection size
        tlengths = [math.pi * (0.21 * self.size), 0.5 * math.pi * (0.625 * self.size), self.size, 0.5 * math.pi * (0.205 * self.size)]
        return cs[0] * tlengths[turn1], cs[1] * tlengths[turn2]


    def tick(self, period):
        # ticks each car and increments the time for period (ms)
        self.time = self.time + period / 1000
        for car in self.cars: car.tick(self.time) # tick each car


    def tkrender(self, canvas, scale):
        # renders intersection and each car on canvas
        x0, y0 = int(canvas.cget("width")) / 2 + self.size / 2 * scale, int(canvas.cget("height")) / 2 - self.size / 2 * scale
        x1, y1 = int(canvas.cget("width")) / 2 - self.size / 2 * scale, int(canvas.cget("height")) / 2 + self.size / 2 * scale
        canvas.create_rectangle(x0, y0, x1, y1, fill="", width=2, outline="grey12")

        for car in self.cars: car.tkrender(self.size, canvas, scale) # render each car