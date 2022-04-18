import math

class Car:
    def __init__(self, id, distance, path, speed):
        self.id = id
        self.distance = distance # distance (m) relative to the enterance of the intersection (negative means approaching intersection)
        self.path = path # tuple containing starting lane and ending lane
        self.speed = speed # speed (m/s) of car relative to path
        self.acceleration = 0 # acceleration (m/s/s) of car relative to path


    def accelerate(self, distance, time):
        # sets acceleration so that car reaches distance in time (ms)
        self.acceleration = ((distance - self.distance) - self.speed * (time * 1000)) * 2 / (time ** 2)


    def time(self, distance):
        # returns time (ms) until car reaches distance (m) based on acceleration
        if self.acceleration == 0: return (distance - self.distance) / self.speed
        return (-self.speed + (self.speed ** 2 + 2 * self.acceleration * (distance - self.distance)) ** 0.5) / self.acceleration


    def tick(self, period):
        # increments time-varying values adjusted for period length (ms)
        self.speed += self.acceleration * (period / 1000)
        self.distance += self.speed * (period / 1000)


    def render(self, size):
        # returns coordinates (m) and direction (rad) realtive to center based on path and distance
        # UPDATES: currently only handles a 1, 3, 5, 7 intersection, need to add direction
        x, y = 0, 0 # relative to the bottom left of starting lane
        seg = size / 4 # all lengths work in quarters, so this is for simplicity
        lin, lout = self.path
        turn = (lout - lin) % 8 // 2 # calculate the modulo difference

        if self.distance <= 0 or turn == 2: # turn does not matter if car is before intersection
            x, y = 3 * seg, self.distance

        elif turn == 0: # U turn
            cut, radius = 1 / 2, seg
            arc = cut * (2 * math.pi * radius) # length of turn
            if self.distance >= arc: x, y = seg, - (self.distance - arc) # if passed intersection
            else: x, y = 2 * seg + radius * math.cos(self.distance / radius), radius * math.sin(self.distance / radius)
            
        elif turn == 1: # left turn
            cut, radius = 1 / 4, 3 * seg
            arc = cut * (2 * math.pi * radius)
            if self.distance >= arc: x, y = - (self.distance - arc), 3 * seg
            else: x, y = radius * math.cos(self.distance / radius), radius * math.sin(self.distance / radius)

        elif turn == 3: # right turn
            cut, radius = 1 / 4, seg
            arc = cut * (2 * math.pi * radius)
            if self.distance >= arc: x, y = 4 * seg + (self.distance - arc), seg
            else: x, y = 4 * seg - radius * math.cos(self.distance / radius), radius * math.sin(self.distance / radius)

        # calculate absolute position
        if lin == 1: return (y - size / 2, size - x - size / 2)
        if lin == 3: return (size - x - size / 2, size - y - size / 2)
        if lin == 5: return (size - y - size / 2, x - size / 2)
        if lin == 7: return (x - size / 2, y - size / 2)
        return (0, 0) # lane not yet implemented




class Intersection:
    def __init__(self, algorithm, size):
        self.algorithm = algorithm
        self.size = size # length (m) of one side of the intersection
        self.time = 0 # clock to track time (ms) elapsed
        self.cars = [] # list of cars monitored by the intersection


    def schedule(self, car):
        # adds new car for intersection to schedule
        self.cars.append(car)
        # based on scheduling algorithm, should assign a car to follow
        return # to be implemented


    def follow(self, car1, car2):
        # sets car1 to pass through intersection immediately after car2
        # if car1 and car2 do not share a critical section, do nothing
        overlap = self.overlap(car1.path, car2.path)
        if overlap == None: return
        car1.accelerate(overlap[0], car2.time(overlap[1]))
        return # to be implemented


    def overlap(self, path1, path2):
        # returns start distance on path1 and end distance on path2 of critical section
        # if there is no critical section, returns None
        # can be implemented as a table for each intersection layout
        return # to be implemented


    def tick(self, period):
        # ticks each car and increments the time
        for car in self.cars: car.tick(period)
        self.time = (self.time + period) % (2 ** 63 - 1)