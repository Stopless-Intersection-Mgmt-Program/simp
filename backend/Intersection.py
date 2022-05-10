import math

# THINGS TO FIX:
# - schedule method should implement rangeTo
# - car should not be allowed to pass through other cars on approach
# - spawn method needs to be implemented

class Intersection:
    def __init__(self):
        self.size = 40 # length (m) of one side of the intersection
        self.speed = 40 # speed (m/s) of cars entering and exiting the intersection
        self.buffer = 0 # gap (s) between cars travelling through intersection

        self.time = 0 # clock to track time (s) elapsed
        self.cars = [] # list of cars monitored by the intersection


    def schedule(self, car):
        # adds car for intersection to handle
        car.time = self.time # synchronize clocks
        vt, dt = self.turnSpeed(car), self.turnLength(car.path)

        # loop through other cars and determine the overall earliest arrival time
        if len(self.cars) > 0: arrival = max(self.earliestArrival(car, c) for c in self.cars)
        else: arrival = 2 * (0 - car.distance) / (car.speed + vt) + self.time
        car.setCourse(0, arrival, vt)

        # set car to go once clear of intersection
        car.accelerate(self.speed - vt, arrival + dt / vt)

        self.cars.append(car)


    def earliestArrival(self, car1, car2):
        # returns earliest time (s) car1 can arrive at the intersection without colliding with car2
        overlap, vt1, vt2 = self.overlap(car1.path, car2.path), self.turnSpeed(car1), self.turnSpeed(car2)
        if overlap == None: return 2 * (0 - car1.distance) / (car1.speed + vt1) + self.time

        else: d1, d2 = overlap # if there is a critical section
        time = car2.atDistance(d2)[0] # time car2 will clear critical section
        if car1.path[1] == car2.path[1] and vt1 > vt2: # if cars are ending in the same lane and rear car is faster
            a1, a2 = car1.acceleration, car2.acceleration
            time += (vt1 - vt2) / a2
            time -= ((self.speed ** 2 - vt2 ** 2) / (2 * a2) - (self.speed ** 2 - vt1 ** 2) / (2 * a1)) / (self.speed)
        return time - d1 / vt1 + self.buffer # adjust time to edge of intersection and add buffer


    def turnSpeed(self, car):
        # returns the speed (m/s) car can take turn based on radius
        li, lo = car.path
        turn = (lo - li) % 4
        if turn == 0: return 0.21 * self.size
        if turn == 1: return 0.625 * self.size
        if turn == 2: return self.speed
        if turn == 3: return 0.205 * self.size

    
    def turnLength(self, path):
        # returns the total distance (m) of the path through the intersection
        li, lo = path
        turn = (lo - li) % 4
        if turn == 0: return math.pi * (0.21 * self.size)
        if turn == 1: return 0.5 * math.pi * (0.625 * self.size)
        if turn == 2: return self.size
        if turn == 3: return 0.5 * math.pi * (0.205 * self.size)


    def overlap(self, path1, path2):
        # returns start distance on path1 and end distance on path2 of critical section
        (li1, lo1), (li2, lo2) = path1, path2
        turn1, turn2 = (lo1 - li1) % 4, (lo2 - li2) % 4
        reld = (li2 - li1) % 4 # relative direction of other car

        if reld == 0: # path1 is path2
            if turn1 // 2 == turn2 // 2: return 0, 8 # if paths have same starting lane
            else: return None # if not in same lane, no critical section

        if reld == 1: # path2 is left of path1
            lcritical = [[None, None, (0, 0.5), (0.8, 1)], # U turn
                        [(0.6, 0.7), (0.5, 0.5), (0, 0.7), None], # left turn
                        [None, None, (0.1, 0.9), None], # straight
                        [None, None, (0.3, 1), None]] # right turn
            cs = lcritical[turn1][turn2]

        if reld == 2: # path2 is opposite of path1
            ocritical = [[None, None, (0.6, 1), None], # U turn
                        [None, None, (0.6, 0.5), None], # left turn
                        [(0.8, 1), (0.3, 1), None, None], # straight
                        [None, None, None, None]] # right turn
            cs = ocritical[turn1][turn2]

        if reld == 3: # path2 is right of path1
            rcritical = [[None, (0.3, 0.9), None, None], # U turn
                        [None, (0.2, 0.7), None, None], # left turn
                        [(0.2, 0.9), (0.5, 0.4), (0.6, 0.3), (0.8, 1)], # straight
                        [(0.3, 1), None, None, None]] # right turn
            cs = rcritical[turn1][turn2]
        if cs == None: return None

        # adjust for intersection size
        return cs[0] * self.turnLength(path1), cs[1] * self.turnLength(path2)


    def spawn(self, distribution):
        # given an array of distributions for the 4 turns, randomly spawns cars and schedules them
        return # to be implemented


    def tick(self, period):
        # ticks each car and increments the time for period (ms)
        self.time = self.time + period / 1000
        for car in self.cars: car.tick(self.time) # tick each car


    def render(self):
        # returns list of car ids, coordinates, and directions
        return [car.render(self.size) for car in self.cars]


    def tkrender(self, canvas, scale):
        # renders intersection and each car on canvas
        x0, y0 = int(canvas.cget("width")) / 2 + self.size / 2 * scale, int(canvas.cget("height")) / 2 - self.size / 2 * scale
        x1, y1 = int(canvas.cget("width")) / 2 - self.size / 2 * scale, int(canvas.cget("height")) / 2 + self.size / 2 * scale
        canvas.create_rectangle(x0, y0, x1, y1, fill="", width=2, outline="grey12")

        for car in self.cars: car.tkrender(self.size, canvas, scale) # render each car